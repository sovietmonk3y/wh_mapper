from django.conf.urls import patterns, url

from wh_mapper.api.system import SystemNameAutocompleteApi
from wh_mapper.api.system_node import SystemNodeCreateAPI, SystemNodeDeleteAPI

urlpatterns = patterns('wh_mapper.views',
    (r'^login/?$', 'login'), #GET, POST
    (r'^$', 'system_map'), #GET
    (r'^(?P<page>[^/.]+)/?$', 'system_map'), #GET
)

urlpatterns += patterns('',
    (r'^api/system/autocomplete/(?P<name_portion>[^/]+)/?$',
        SystemNameAutocompleteApi.as_view()), #GET
)

urlpatterns += patterns('',
    (r'^api/system_node/$', SystemNodeCreateAPI.as_view()), #POST
    (r'^api/system_node/(?P<page_name>[^/]+)/(?P<node_id>[^/]+)/?$',
        SystemNodeDeleteAPI.as_view()), #DELETE
)
