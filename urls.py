from django.conf.urls import patterns, url

from wh_mapper.api.system import SystemNameAutocompleteApi
import wh_mapper.api.system_connection as system_connection_api
import wh_mapper.api.system_node as system_node_api

urlpatterns = patterns('wh_mapper.views',
    (r'^login/$', 'login'), #GET, POST
    (r'^$', 'system_map'), #GET
    (r'^(?P<page>[^/.]+)/$', 'system_map'), #GET
)

urlpatterns += patterns('',
    (r'^api/system/autocomplete/(?P<name_portion>[^/]+)/$',
        SystemNameAutocompleteApi.as_view()), #GET
)

urlpatterns += patterns('',
    (r'^api/system_connection/$',
        system_connection_api.SystemConnectionCreateAPI.as_view()), #POST
    (r'^api/system_connection/(?P<connection_id>[^/]+)/$',
        system_connection_api.SystemConnectionEditAPI.as_view()), #PUT

    (r'^api/system_node/$',
        system_node_api.SystemNodeCreateAPI.as_view()), #POST
    (r'^api/system_node/(?P<page_name>[^/]+)/(?P<node_id>[^/]+)/$',
        system_node_api.SystemNodeEditAPI.as_view()), #PUT, DELETE
)
