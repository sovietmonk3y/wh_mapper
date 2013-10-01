import os
import sys
sys.path.append('/'.join(os.path.abspath(__file__).split('/')[:-2]))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wh_mapper.settings")

from datetime import timedelta
import json

from django.conf import settings as django_settings
import django.contrib.auth as django_auth
import django.core.handlers.wsgi as django_wsgi
from django.utils.importlib import import_module

from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging
import tornado.web as tornado_web
from tornado.wsgi import WSGIContainer

import wh_mapper.forms as wh_mapper_forms
import wh_mapper.models as wh_mapper_models
from wh_mapper.tornado_vars import node_locks, pulses

#USE CACHING...
pulses[''] = {}
for page_name in (wh_mapper_models.SystemNode.objects.all()
                                          .values_list('page_name', flat=True)):
    node_locks[page_name] = {}
    pulses[page_name] = {}

def store_django_user(request_handler):
    request_handler.session = import_module(
        django_settings.SESSION_ENGINE).SessionStore(request_handler.get_cookie(
            django_settings.SESSION_COOKIE_NAME))
    request_handler.user = django_auth.get_user(request_handler)


class UpdatesAPI(tornado_web.RequestHandler):
    @tornado_web.asynchronous
    def send_update(self, node_lock=None, new_page=None, new_node=None,
                    delete_page=None, delete_node=None):
        if (self.page_name in pulses and
            self.user.username in pulses[self.page_name]):
            IOLoop.instance().remove_timeout(
                pulses[self.page_name][self.user.username])
        else:
            return

        if self.request.connection.stream.closed():
            del pulses[self.page_name][self.user.username]
        else:
            data = {'user_list' :
                list(set([user for page in pulses for user in pulses[page]]))}
            if node_lock: data.update({'node_lock' : node_lock})
            if new_page: data.update({'new_page' : new_page})
            elif new_node: data.update({'new_node' : new_node})
            elif delete_page: data.update({'delete_page' : delete_page})
            elif delete_node: data.update({'delete_node' : delete_node})
            self.finish(data)

    @tornado_web.asynchronous
    def send_update_timeout(self):
        ioloop = IOLoop.instance()
        for page in pulses:
            if self.user.username in pulses[page]:
                ioloop.remove_timeout(pulses[page][self.user.username])
                del pulses[page][self.user.username]
                break
        pulses[self.page_name][self.user.username] = ioloop.add_timeout(
            timedelta(seconds=30), self.send_update)

    @tornado_web.asynchronous
    def get(self, page_name):
        store_django_user(self)
        if self.user.is_authenticated():
            if page_name in pulses:
                self.page_name = page_name
                IOLoop.instance().add_callback(self.send_update_timeout)
            else:
                self.set_status(400, 'Invalid page')
                self.finish()
        else:
            self.redirect('/login/')


class SystemNodeLockAPI(tornado_web.RequestHandler):
    @tornado_web.asynchronous
    def post(self):
        store_django_user(self)
        if self.user.is_authenticated():
            if ('node_id' in self.request.arguments and
                'page_name' in self.request.arguments):
                node_id = self.get_argument('node_id')
                page_name = self.get_argument('page_name')
                node_lock_form = wh_mapper_forms.NodeLockCreateForm(
                    {'node_id' : node_id, 'page_name' : page_name})
                if node_lock_form.is_valid():
                    if not node_id:
                        if self.user.username in node_locks[page_name]:
                            self.finish()
                            node_id = node_locks[page_name][self.user.username]
                            del node_locks[page_name][self.user.username]
                            for user in pulses[page_name]:
                                if user != self.user.username:
                                    send_update = (
                                        pulses[page_name][user].callback)
                                    send_update(node_lock={'username' : None,
                                                           'node_id' : node_id})
                        else:
                            self.set_status(400, 'You do not have any node ' +
                                                 'locks')
                            self.finish()
                    elif (self.user.username in node_locks[page_name] and
                          node_locks[page_name][self.user.username] == node_id):
                        self.set_status(400, 'You are already interacting ' +
                                             'with that node')
                        self.finish()
                    elif node_id in node_locks[page_name].values():
                        self.set_status(400, 'The node you are attempting to ' +
                                      'interact with is locked by someone else')
                        self.finish()
                    else:
                        node_locks[page_name][self.user.username] = node_id
                        self.finish()
                        for user in pulses[page_name]:
                            if user != self.user.username:
                                send_update = pulses[page_name][user].callback
                                send_update(node_lock={
                                        'username' : self.user.username,
                                        'node_id' : node_id})
                else:
                    self.set_status(400, node_lock_form.errors.as_text())
                    self.finish()
            else:
                self.set_status(400, 'Invalid node lock request')
                self.finish()
        else:
            self.redirect('/login/')


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
