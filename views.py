import json

import django.contrib.auth as contrib_auth
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response

from tornado.ioloop import IOLoop

import wh_mapper.constants as constants
import wh_mapper.models as wh_mapper_models
from wh_mapper.tornado_vars import node_locks, pulses

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            user = contrib_auth.authenticate(username=username,
                                             password=password)
            if user:
                contrib_auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseBadRequest('Invalid account')
        else:
            return render_to_response('login.html')

def system_map(request, page=None):
    if request.user.is_authenticated():
        if page:
            for page_name in node_locks:
                if request.user.username in node_locks[page_name]:
                    node_id = node_locks[page_name][request.user.username]
                    del node_locks[page_name][request.user.username]
                    for user in pulses[page_name]:
                        if user != request.user.username:
                            send_update = (
                                pulses[page_name][user].callback)
                            IOLoop.instance().add_callback(send_update,
                                node_lock={'username' : None,
                                           'node_id' : node_id})
                    break

        nodes = wh_mapper_models.SystemNode.objects.select_related(
            'system', 'parent_connection__wormhole').order_by('parent_node')
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
                    if node_tree.has_key(node.parent_node_id):
                        node_tree[node.parent_node_id]['children'][node.id] = (
                            node_tree[node.id].copy())
                    else:
                        node_tree[node.parent_node_id] = {
                            'children' : {node.id : node_tree[node.id].copy()}}

            endpoint_id_list = [node_id for node_id in node_tree
                                if node_tree[node_id]['children'] == {}]
            node_tree_width = len(endpoint_id_list)
            for endpoint_id in endpoint_id_list:
                current_node = node_tree[endpoint_id]
                length = 0

                while current_node:
                    if current_node['parent_node_id']:
                        current_parent_node_id = current_node['parent_node_id']

                        if node_tree.has_key(current_parent_node_id):
                            node_tree[current_parent_node_id]['children'][
                                current_node['id']]['children'] = sorted(
                                current_node['children'].values(),
                                key=lambda x:x['date'])

                        if (not node_tree.has_key(current_parent_node_id) or
                            not current_node['children'] or
                            not set(current_node['children'].keys())
                                .intersection(node_tree.keys())):
                            del node_tree[current_node['id']]

                        current_node = node_tree.get(current_parent_node_id,
                                                     None)
                    else:
                        current_node = None
                    length += 1
                    if length > node_tree_length: node_tree_length = length

            node_tree = node_tree.values()[0]
            node_tree['children'] = sorted(node_tree['children'].values(),
                                           key=lambda x:x['date'])

        template_vars = {'system_tree': json.dumps(node_tree),
                         'system_tree_length': node_tree_length,
                         'system_tree_width': node_tree_width,
                         'page': page,
                         'map_pages': map_pages,
                         'user_list': list(set([user for pulse_page in pulses
                                                for user in pulses[pulse_page]])
                                           .union([request.user.username])),
                         'node_locks': json.dumps([
                             {'node_id' : node_locks[page][username],
                              'username' : username}
                             for username in node_locks.get(page, {})]),
                         'WORMHOLE_SIG_LENGTH' :
                             constants.WORMHOLE_SIG_MAX_LENGTH,
                         'WORMHOLE_LIFE_LEVELS' :
                             constants.WORMHOLE_LIFE_LEVELS,
                         'WORMHOLE_MASS_LEVELS' :
                             constants.WORMHOLE_MASS_LEVELS,
                         'WORMHOLE_LIFE_PERCENTAGES' :
                             constants.WORMHOLE_LIFE_PERCENTAGES,
                         'WORMHOLE_MASS_PERCENTAGES' :
                             constants.WORMHOLE_MASS_PERCENTAGES}

        return render_to_response('map.html', template_vars)
    else:
        return HttpResponseRedirect('/login/')
