import json

from django.contrib.auth.models import User
from django.test import Client, TestCase

import wh_mapper.models as wh_mapper_models

class TestUtilities():
    username = 'testuser'
    password = 'password'

    def __init__(self):
        User.objects.create_user(username=self.username, password=self.password)

    def get_logged_in_client(self):
        logged_in_client = Client()
        logged_in_client.login(username=self.username, password=self.password)
        return logged_in_client

    def create_test_root_node(self, system, page_name):
        test_root_node = wh_mapper_models.SystemNode(
            author_username=self.username, system_name=system,
            page_name=page_name)
        test_root_node.save()
        return test_root_node


class SystemNodeCreateAPITestCase(TestCase):
    url = '/api/system_node/'
    data = {'system': 'jita', 'page_name': 'testpage'}

    def test_create_node_no_auth(self):
        response = self.client.post(self.url, self.data)
        self.assertNotEqual(response.status_code, 200)
        try:
            wh_mapper_models.SystemNode.objects.get(**self.data)
            raise self.failureException('System node object was created')
        except:
            pass

    def test_create_root_node(self):
        response = TestUtilities().get_logged_in_client().post(
            self.url, self.data)
        self.assertEqual(response.status_code, 200)
        system_node = wh_mapper_models.SystemNode.objects.get(**self.data)
        self.assertEqual(system_node.parent_node_id, None)

    def test_create_root_node_same_page(self):
        util = TestUtilities()
        util.create_test_root_node(self.data['system'], self.data['page_name'])
        response = util.get_logged_in_client().post(self.url, self.data)
        self.assertEqual(response.status_code, 400)
        try:
            wh_mapper_models.SystemNode.objects.get(**data)
            raise self.failureException('Root node object was created')
        except:
            pass

    def test_create_child_node(self):
        util = TestUtilities()
        data = self.data.copy()
        data['parent_node'] = util.create_test_root_node(self.data['system'],
            self.data['page_name']).id
        response = util.get_logged_in_client().post(self.url, data)
        self.assertEqual(response.status_code, 200)
        wh_mapper_models.SystemNode.objects.get(**data)

    def test_create_node_missing_system(self):
        data = self.data.copy()
        del data['system']
        response = TestUtilities().get_logged_in_client().post(
            self.url, data)
        self.assertEqual(response.status_code, 400)
        try:
            wh_mapper_models.SystemNode.objects.get(**data)
            raise self.failureException('System node object was created')
        except:
            pass

    def test_create_node_missing_page(self):
        data = self.data.copy()
        del data['page_name']
        response = TestUtilities().get_logged_in_client().post(
            self.url, data)
        self.assertEqual(response.status_code, 400)
        try:
            wh_mapper_models.SystemNode.objects.get(**data)
            raise self.failureException('System node object was created')
        except:
            pass

    def test_create_node_invalid_system(self):
        data = self.data.copy()
        data['system'] = '         '
        response = TestUtilities().get_logged_in_client().post(
            self.url, data)
        self.assertEqual(response.status_code, 400)
        try:
            wh_mapper_models.SystemNode.objects.get(**data)
            raise self.failureException('System node object was created')
        except:
            pass

    def test_create_node_invalid_parent(self):
        data = self.data.copy()
        data['parent_node'] = 'invalid parent'
        response = TestUtilities().get_logged_in_client().post(
            self.url, data)
        self.assertEqual(response.status_code, 400)
        try:
            wh_mapper_models.SystemNode.objects.get(**data)
            raise self.failureException('System node object was created')
        except:
            pass


class SystemNodeDeleteAPITestCase(TestCase):
    url = '/api/system_node/'
    data = {'system': 'jita', 'page_name': 'testpage'}

    def test_delete_node_no_auth(self):
        util = TestUtilities()
        test_root_node_id = util.create_test_root_node(self.data['system'],
            self.data['page_name']).id
        response = self.client.delete(self.url + test_root_node_id + '/')
        self.assertNotEqual(response.status_code, 200)
        wh_mapper_models.SystemNode.objects.get(id=test_root_node_id)

    def test_delete_root_node(self):
        util = TestUtilities()
        test_root_node_id = util.create_test_root_node(self.data['system'],
            self.data['page_name']).id
        response = util.get_logged_in_client().delete(self.url +
                                                      test_root_node_id + '/')
        self.assertEqual(response.status_code, 200)
        try:
            wh_mapper_models.SystemNode.objects.get(id=test_root_node_id)
            raise self.failureException('System node object was not deleted')
        except:
            pass

    def test_delete_node_chain(self):
        util = TestUtilities()
        node = util.create_test_root_node(self.data['system'],
                                          self.data['page_name'])

        node_id_list = []
        for i in range(5):
            node.parent_node_id = node.id
            node.id = ''
            node.date = ''
            node.save()
            node_id_list.append(node.id)

        response = util.get_logged_in_client().delete(self.url +
                                                      node_id_list[0] + '/')
        self.assertEqual(response.status_code, 200)
        if wh_mapper_models.SystemNode.objects.filter(id__in=node_id_list):
            raise self.failureException('System node objects were not deleted')

    def test_delete_node_invalid_id(self):
        response = TestUtilities().get_logged_in_client().delete(
            self.url + 'invalid id' + '/')
        self.assertEqual(response.status_code, 400)


class SystemNameAutocompleteApiTestCase(TestCase):
    url = '/api/system/autocomplete/'

    def test_autocomplete_no_auth(self):
        response = self.client.get(self.url + 'jit' + '/')
        self.assertNotEqual(response.status_code, 200)

    def test_autocomplete(self):
        response = TestUtilities().get_logged_in_client().get(self.url + 'jit' +
                                                              '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)[0], 'Jita')
