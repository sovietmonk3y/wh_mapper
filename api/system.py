import json

from django.http import HttpResponse, HttpResponseBadRequest,\
                        HttpResponseRedirect
from django.views.generic.base import View

from wh_mapper.constants import SYSTEM_NAME_AUTOCOMPLETE_MAX_RESULTS
import wh_mapper.models as wh_mapper_models

class SystemNameAutocompleteApi(View):

    def get(self, request, name_portion):
        if request.user.is_authenticated():
            if name_portion.strip() == '':
                return HttpResponseBadRequest(
                    'Invalid text supplied for autocompletion')

            systems = wh_mapper_models.System.objects.filter(
                name__istartswith=name_portion).values_list(
                'name', flat=True)[:SYSTEM_NAME_AUTOCOMPLETE_MAX_RESULTS]
            return HttpResponse(json.dumps(list(systems)))
        else:
            return HttpResponseRedirect('/login/')
