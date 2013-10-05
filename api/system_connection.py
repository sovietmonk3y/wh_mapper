import json

import django.http as django_http
from django.views.generic.base import View

from tornado.ioloop import IOLoop

import wh_mapper.forms as wh_mapper_forms
import wh_mapper.models as wh_mapper_models
from wh_mapper.tornado_vars import node_locks, pulses

class SystemConnectionCreateAPI(View):

    def post(self, request):
        if request.user.is_authenticated():
            data = request.POST.copy()
            data['author'] = request.user.username

            connection_form = wh_mapper_forms.SystemConnectionCreateForm(data)
            node_form = wh_mapper_forms.SystemNodeCreateForm(data)
            if connection_form.is_valid():
                connection_form.instance.facing_down = (
                    connection_form.instance.wormhole.sig != 'K162')

                system_connection = connection_form.save()

                node_form.instance.parent_connection_id = system_connection.id
                child_node = node_form.save()

                del node_locks[child_node.page_name][request.user.username]

                node_json = child_node.json_safe()
                node_json['children'] = []

                update_data = {'node_lock' :
                                   {'username' : None,
                                    'node_id' : child_node.parent_node_id},
                               'new_node' : node_json}
                for user in pulses[child_node.page_name]:
                    if user != request.user.username:
                        send_update = (
                            pulses[child_node.page_name][user].callback)
                        IOLoop.instance().add_callback(send_update,
                            **update_data)

                return django_http.HttpResponse(json.dumps(node_json))
            else:
                return django_http.HttpResponseBadRequest(
                    connection_form.errors.as_text())
        else:
            return django_http.HttpResponseRedirect('/login/')


class SystemConnectionEditAPI(View):

    def put(self, request, connection_id):
        if request.user.is_authenticated():
            connection = None
            try:
                connection = wh_mapper_models.SystemConnection.objects.get(
                    id=connection_id)
            except wh_mapper_models.SystemConnection.DoesNotExist:
                return django_http.HttpResponseBadRequest(
                    'System connection does not exist')

            data = django_http.request.QueryDict(request.body).copy()
            data['author'] = request.user.username
            edit_form = wh_mapper_forms.SystemConnectionEditForm(data,
                instance=connection)
            if edit_form.is_valid():
                connection = edit_form.save()
                connection_json = connection.json_safe()
                connection_json['wormhole_type'] = connection.wormhole.type

                page = None
                for page in pulses:
                    if request.user.username in pulses[page]:
                        break
                for user in pulses[page]:
                    if user != request.user.username:
                        send_update = (
                            pulses[page][user].callback)
                        IOLoop.instance().add_callback(send_update,
                            update_connection=connection_json)

                return django_http.HttpResponse(json.dumps(connection_json))
            else:
                return django_http.HttpResponseBadRequest(
                    edit_form.errors.as_text())
        else:
            return django_http.HttpResponseRedirect('/login/')
