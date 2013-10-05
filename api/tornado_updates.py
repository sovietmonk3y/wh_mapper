from datetime import timedelta

from tornado.ioloop import IOLoop
import tornado.web as tornado_web

from wh_mapper.lib.tornado import store_django_user
from wh_mapper.tornado_vars import pulses

class UpdatesAPI(tornado_web.RequestHandler):
    def send_update(self, **kwargs):
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

            if 'node_lock' in kwargs:
                data['node_lock'] = kwargs['node_lock']

            if 'new_page' in kwargs:
                data['new_page'] = kwargs['new_page']
            elif 'new_node' in kwargs:
                data['new_node'] = kwargs['new_node']
            elif 'delete_page' in kwargs:
                data['delete_page'] = kwargs['delete_page']
            elif 'delete_node' in kwargs:
                data['delete_node'] = kwargs['delete_node']
            elif 'update_node' in kwargs:
                data['update_node'] = kwargs['update_node']
            elif 'update_connection' in kwargs:
                data['update_connection'] = kwargs['update_connection']

            self.finish(data)

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
