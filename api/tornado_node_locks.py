from tornado.ioloop import IOLoop
import tornado.web as tornado_web

import wh_mapper.forms as wh_mapper_forms

from wh_mapper.lib.tornado import store_django_user
from wh_mapper.tornado_vars import node_locks, pulses

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
                                    IOLoop.instance().add_callback(send_update,
                                        node_lock={'username' : None,
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
                                IOLoop.instance().add_callback(send_update,
                                    node_lock={'username' : self.user.username,
                                               'node_id' : node_id})
                else:
                    self.set_status(400, node_lock_form.errors.as_text())
                    self.finish()
            else:
                self.set_status(400, 'Invalid node lock request')
                self.finish()
        else:
            self.redirect('/login/')
