import json

import django.http as django_http
from django.views.generic.base import View

from tornado.ioloop import IOLoop

import wh_mapper.forms as wh_mapper_forms
import wh_mapper.models as wh_mapper_models
from wh_mapper.tornado_vars import object_locks, pulses

class SystemNodeCreateAPI(View):

    def post(self, request):
        if request.user.is_authenticated():
            data = request.POST.copy()
            data['author'] = request.user.username
            create_form = wh_mapper_forms.SystemNodeCreateForm(data)
            if create_form.is_valid():
                new_node = create_form.save()
                node_json = new_node.json_safe()
                node_json['children'] = []

                if new_node.page_name in pulses:
                    del object_locks[new_node.page_name][request.user.username]
                    for user in pulses[new_node.page_name]:
                        if user != request.user.username:
                            send_update = (
                                pulses[new_node.page_name][user].callback)
                            IOLoop.instance().add_callback(send_update,
                                object_lock={'id' : new_node.parent_node_id,
                                             'type' : 'node'},
                                new_node=node_json)
                else:
                    pulses[new_node.page_name] = {}
                    object_locks[new_node.page_name] = {}
                    for update_timeout in [
                        pulses[page][user] for page in pulses
                        for user in pulses[page]
                        if user != request.user.username]:
                        send_update = update_timeout.callback
                        IOLoop.instance().add_callback(send_update,
                            new_page=new_node.page_name)

                return django_http.HttpResponse(json.dumps(node_json))
            else:
                return django_http.HttpResponseBadRequest(
                    create_form.errors.as_text())
        else:
            return django_http.HttpResponseRedirect('/login/')


class SystemNodeEditAPI(View):

    def put(self, request, page_name, node_id):
        if request.user.is_authenticated():
            node = None
            try:
                node = wh_mapper_models.SystemNode.objects.get(
                    id=node_id, page_name=page_name)
            except wh_mapper_models.SystemNode.DoesNotExist:
                return django_http.HttpResponseBadRequest(
                    'System node does not exist')

            data = django_http.request.QueryDict(request.body).copy()
            data['author'] = request.user.username
            edit_form = wh_mapper_forms.SystemNodeEditForm(data, instance=node)
            if edit_form.is_valid():
                edit_form.instance.date = None
                node = edit_form.save()
                node_json = node.json_safe()

                del object_locks[page_name][request.user.username]
                for user in pulses[page_name]:
                    if user != request.user.username:
                        send_update = (
                            pulses[page_name][user].callback)
                        IOLoop.instance().add_callback(send_update,
                            object_lock={'type' : 'node', 'id' : node_id},
                            update_node=node_json)

                return django_http.HttpResponse(json.dumps(node_json))
            else:
                return django_http.HttpResponseBadRequest(
                    edit_form.errors.as_text())
        else:
            return django_http.HttpResponseRedirect('/login/')

    #@transaction.atomic -------- ADD THIS IN DJANGO 1.6
    def delete(self, request, page_name, node_id):
        if request.user.is_authenticated():
            node_id_dict_list = wh_mapper_models.SystemNode.objects.filter(
                page_name=page_name).order_by('parent_node').values(
                'id', 'parent_node_id', 'parent_connection_id')

            if not node_id_dict_list:
                return django_http.HttpResponseBadRequest('Invalid page')

            node_id_valid = False
            for node_id_dict in node_id_dict_list:
                if node_id_dict['id'] == node_id:
                    node_id_valid = True
                    break
            if not node_id_valid:
                return django_http.HttpResponseBadRequest('Invalid node ID')

            node_delete_id_list = [node_id]
            current_level_id_list = node_delete_id_list
            while current_level_id_list:
                current_level_id_list = [id_dict['id'] for id_dict in
                                         node_id_dict_list if
                                         id_dict['parent_node_id'] in
                                         current_level_id_list]
                if current_level_id_list:
                    node_delete_id_list.extend(current_level_id_list)

            connection_delete_id_list = [id_dict['parent_connection_id']
                                         for id_dict in node_id_dict_list if
                                         id_dict['id'] in node_delete_id_list]

            object_lock_id_list = [lock['id'] for lock in
                                   object_locks[page_name].values()]
            if (len(set(node_delete_id_list).intersection(
                object_lock_id_list)) > 1 or
                set(connection_delete_id_list).intersection(
                    object_lock_id_list)):
                return django_http.HttpResponseBadRequest(
                    'Cannot delete a node whose descendant is currently locked')

            wh_mapper_models.SystemNode.objects.filter(
                id__in=node_delete_id_list).delete()

            wh_mapper_models.SystemConnection.objects.filter(
                id__in=connection_delete_id_list).delete()

            if node_id_dict_list[0]['id'] == node_id:
                del object_locks[page_name]
                for update_timeout in [pulses[page][user] for page in pulses
                                       for user in pulses[page]
                                       if user != request.user.username]:
                    send_update = update_timeout.callback
                    IOLoop.instance().add_callback(send_update,
                        delete_page=page_name)
                del pulses[page_name]
            elif page_name in pulses:
                del object_locks[page_name][request.user.username]
                for user in pulses[page_name]:
                    if user != request.user.username:
                        send_update = pulses[page_name][user].callback
                        IOLoop.instance().add_callback(send_update,
                            delete_node=node_id)

            return django_http.HttpResponse()
        else:
            return django_http.HttpResponseRedirect('/login/')
