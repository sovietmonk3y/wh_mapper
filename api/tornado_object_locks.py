from tornado.ioloop import IOLoop
import tornado.web as tornado_web

import wh_mapper.forms as wh_mapper_forms

from wh_mapper.lib.tornado import store_django_user
import wh_mapper.models as wh_mapper_models
from wh_mapper.tornado_vars import object_locks, pulses

class MapObjectLockAPI(tornado_web.RequestHandler):
    @tornado_web.asynchronous
    def post(self):
        store_django_user(self)
        if self.user.is_authenticated():
            if (('node_id' in self.request.arguments or
                 'connection_id' in self.request.arguments) and
                'page_name' in self.request.arguments):
                object_id = None
                object_type = None
                page_name = self.get_argument('page_name')

                if 'node_id' in self.request.arguments:
                    object_id = self.get_argument('node_id')
                    object_type = 'node'
                else:
                    object_id = self.get_argument('connection_id')
                    object_type = 'connection'

                if page_name in object_locks:
                    if not object_id:
                        if self.user.username in object_locks[page_name]:
                            self.finish()
                            object_id = object_locks[page_name][
                                self.user.username]['id']
                            object_type = object_locks[page_name][
                                self.user.username]['type']
                            del object_locks[page_name][self.user.username]
                            for user in pulses[page_name]:
                                if user != self.user.username:
                                    send_update = (
                                        pulses[page_name][user].callback)
                                    IOLoop.instance().add_callback(send_update,
                                        object_lock={'id' : object_id,
                                            'type' : object_type})
                        else:
                            self.set_status(400, 'You do not have any object ' +
                                                 'locks')
                            self.finish()
                        return
                    elif (self.user.username in object_locks[page_name] and
                          object_locks[page_name][self.user.username]['id'] ==
                          object_id):
                        self.set_status(400, 'You are already interacting ' +
                            'with that object')
                        self.finish()
                        return
                    elif object_id in [lock['id'] for lock in
                                       object_locks[page_name].values()]:
                        self.set_status(400, 'The object you are attempting ' +
                            'to interact with is locked by someone else')
                        self.finish()
                        return
                else:
                    self.set_status(400, 'Invalid page')
                    self.finish()
                    return

                node_id_dict_list = wh_mapper_models.SystemNode.objects.filter(
                    page_name=page_name).values('id', 'parent_node_id',
                                                'parent_connection_id')

                if not node_id_dict_list:
                    self.set_status(400, 'Invalid page')
                    self.finish()
                    return

                family_id_list = []

                object_id_valid = False
                for node_id_dict in node_id_dict_list:
                    if (object_type == 'node' and
                        node_id_dict['id'] == object_id):
                        family_id_list.append(object_id)
                        object_id_valid = True
                        break
                    elif (object_type == 'connection' and
                          node_id_dict['parent_connection_id'] == object_id):
                        family_id_list.append(node_id_dict['id'])
                        family_id_list.append(object_id)
                        object_id_valid = True
                        break

                if not object_id_valid:
                    self.set_status(400, 'Invalid map object')
                    self.finish()
                    return

                if object_type == 'node':
                    current_level_id_list = family_id_list
                    while current_level_id_list:
                        temp_list = []
                        for id_dict in node_id_dict_list:
                            if (id_dict['parent_node_id'] in
                                current_level_id_list):
                                temp_list.append(id_dict['id'])
                                if id_dict['parent_connection_id']:
                                    temp_list.append(
                                        id_dict['parent_connection_id'])
                        current_level_id_list = temp_list
                        if current_level_id_list:
                            family_id_list.extend(current_level_id_list)

                    currentParentID = family_id_list[0]
                    while currentParentID:
                        tempID = currentParentID
                        currentParentID = None
                        for id_dict in node_id_dict_list:
                            if id_dict['id'] == tempID:
                                currentParentID = id_dict['parent_node_id']
                                family_id_list.append(currentParentID)
                                break

                object_lock_id_list = [object_locks[page_name][user]['id']
                                       for user in object_locks[page_name] if
                                       user != self.user.username]

                if set(family_id_list).intersection(object_lock_id_list):
                    self.set_status(400, 'Cannot lock an object that is ' +
                                    'related to a locked object')
                    self.finish()
                    return

                object_locks[page_name][self.user.username] = {
                    'id' : object_id, 'type' : object_type}
                self.finish()
                for user in pulses[page_name]:
                    if user != self.user.username:
                        send_update = pulses[page_name][user].callback
                        IOLoop.instance().add_callback(send_update,
                            object_lock={'username' : self.user.username,
                                'type' : object_type, 'id' : object_id})
            else:
                self.set_status(400, 'Invalid object lock request')
                self.finish()
        else:
            self.redirect('/login/')
