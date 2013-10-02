import os
import sys
sys.path.append('/'.join(os.path.abspath(__file__).split('/')[:-2]))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wh_mapper.settings")

import django.core.handlers.wsgi as django_wsgi

from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging
import tornado.web as tornado_web
from tornado.wsgi import WSGIContainer

from wh_mapper.api.tornado_node_locks import SystemNodeLockAPI
from wh_mapper.api.tornado_updates import UpdatesAPI
import wh_mapper.models as wh_mapper_models
from wh_mapper.tornado_vars import node_locks, pulses

#USE CACHING...
pulses[''] = {}
for page_name in (wh_mapper_models.SystemNode.objects.all().values_list(
        'page_name', flat=True)):
    node_locks[page_name] = {}
    pulses[page_name] = {}

if __name__ == '__main__':
    wsgi_app = WSGIContainer(django_wsgi.WSGIHandler())
    tornado_web.Application(
        [
            (r'/get_updates/([^/]*)/', UpdatesAPI),
            (r'/lock_node/', SystemNodeLockAPI),
            (r'.*', tornado_web.FallbackHandler, dict(fallback=wsgi_app))
        ],
        static_path='static').listen(8000)
    enable_pretty_logging()
    IOLoop.instance().start()
