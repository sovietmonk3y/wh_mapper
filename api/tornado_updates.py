from datetime import timedelta

from tornado.ioloop import IOLoop
import tornado.web as tornado_web

from wh_mapper.lib.tornado import store_django_user
from wh_mapper.tornado_vars import pulses

class UpdatesAPI(tornado_web.RequestHandler):
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
            if node_lock: data.update(node_lock=node_lock)
            if new_page: data.update(new_page=new_page)
            elif new_node: data.update(new_node=new_node)
            elif delete_page: data.update(delete_page=delete_page)
            elif delete_node: data.update(delete_node=delete_node)
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
