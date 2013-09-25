from django.http import HttpResponse, HttpResponseBadRequest,\
                        HttpResponseRedirect
from django.views.generic.base import View

import wh_mapper.forms as wh_mapper_forms
import wh_mapper.models as wh_mapper_models

class SystemNodeCreateAPI(View):

    def post(self, request):
        if request.user.is_authenticated():
            data = request.POST.copy()
            data['author'] = request.user.username
            create_form = wh_mapper_forms.SystemNodeCreateForm(data)
            if create_form.is_valid():
                create_form.save()
                return HttpResponse()
            else:
                return HttpResponseBadRequest(create_form.errors.as_text())
        else:
            return HttpResponseRedirect('/login/')


class SystemNodeDeleteAPI(View):

    def delete(self, request, node_id):
        if request.user.is_authenticated():
            node_id_dict_list = (wh_mapper_models.SystemNode.objects
                                                .values('id', 'parent_node_id'))

            node_id_valid = False
            for node_id_dict in node_id_dict_list:
                if node_id_dict['id'] == node_id:
                    node_id_valid = True
                    break
            if not node_id_valid:
                return HttpResponseBadRequest('Invalid system ID')

            node_delete_id_list = [node_id]
            current_level_id_list = node_delete_id_list
            while current_level_id_list:
                current_level_id_list = [id_dict['id'] for id_dict in
                                         node_id_dict_list if
                                         id_dict['parent_node_id'] in
                                         current_level_id_list]
                if current_level_id_list:
                    node_delete_id_list.extend(current_level_id_list)

            wh_mapper_models.SystemNode.objects.filter(
                id__in=node_delete_id_list).delete()

            return HttpResponse()
        else:
            return HttpResponseRedirect('/login/')
