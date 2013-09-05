import json

from django.shortcuts import render_to_response

from wh_mapper.constants import SYSTEM_TYPE_CHOICES
import wh_mapper.models as wh_mapper_models

def system_map(request, page=None):
    nodes = wh_mapper_models.SystemNode.objects.all().order_by('parent_node', 'date')
    map_pages = set([node.page_name for node in nodes])
    if page:
        nodes = [node for node in nodes if node.page_name == page]
    else:
        nodes = []

    node_tree = {}
    node_tree_length = 0
    node_tree_width = 0
    if nodes:
        for node in nodes:
            if not node_tree.has_key(node.id):
                node_tree[node.id] = node.json_safe()
                node_tree[node.id]['children'] = {}
            elif len(node_tree[node.id]) == 1:
                node_tree[node.id].update(node.json_safe())

            if node.parent_node_id:
                node_tree[node.id]['parent_node_id'] = node.parent_node_id
                if node_tree.has_key(node.parent_node_id):
                    node_tree[node.parent_node_id]['children'][node.id] = node.json_safe()
                else:
                    node_tree[node.parent_node_id] = {'children' : {node.id : node.json_safe()}}

        endpoint_id_list = [node_id for node_id in node_tree if node_tree[node_id]['children'] == {}]
        node_tree_width = len(endpoint_id_list)
        for endpoint_id in endpoint_id_list:
            current_node = node_tree[endpoint_id]
            length = 0

            while current_node:
                if current_node.has_key('parent_node_id'):
                    current_parent_node_id = current_node['parent_node_id']
                    if node_tree.has_key(current_parent_node_id) and current_node['children']:
                        node_tree[current_parent_node_id]['children'][current_node['id']]['children'] = current_node['children'].values()
                    if not (node_tree.has_key(current_parent_node_id) and current_node['children'] and set(current_node['children'].keys()).intersection(set(node_tree.keys()))):
                        del node_tree[current_node['id']]
                    current_node = node_tree.get(current_parent_node_id, None)
                else:
                    current_node = None
                length += 1
                if length > node_tree_length: node_tree_length = length

        node_tree = node_tree.values()[0]
        node_tree['children'] = node_tree['children'].values()

    template_vars = {'system_tree': json.dumps(node_tree),
                     'system_tree_length': node_tree_length,
                     'system_tree_width': node_tree_width,
                     'page': page,
                     'map_pages': map_pages,
                     'SYSTEM_TYPES': SYSTEM_TYPE_CHOICES}

    return render_to_response('map.html', template_vars)
