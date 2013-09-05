from django.test import TestCase

import wh_mapper.models as wh_mapper_models

class SystemNodeTestUtilities():

    def create_test_root_node(self):
        test_root_node = wh_mapper_models.SystemNode(author='testuser',
                                                     name='Testville',
                                                     type='high',
                                                     page_name='testpage')
        test_root_node.save()
        return test_root_node.id


class SystemNodeCreateAPITestCase(TestCase):
    url = '/api/system_node/'
    data = {'author': 'testuser', 'name': 'Testville', 'type': 'high',
            'page_name': 'testpage'}

    def test_create_root_node(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        system_node = wh_mapper_models.SystemNode.objects.get(**self.data)
        self.assertEqual(system_node.parent_node_id, None)

    def test_create_child_node(self):
        util = SystemNodeTestUtilities()
        data = self.data.copy()
        data['parent_node'] = util.create_test_root_node()
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        wh_mapper_models.SystemNode.objects.get(**data)

    def test_create_node_missing_author(self):
        data = self.data.copy()
        del data['author']
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        try:
            wh_mapper_models.SystemNode.objects.get(**data)
            raise self.failureException('System node object was created')
        except:
            pass

    def test_create_node_missing_name(self):
        data = self.data.copy()
        del data['name']
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        try:
            wh_mapper_models.SystemNode.objects.get(**data)
            raise self.failureException('System node object was created')
        except:
            pass

    def test_create_node_missing_type(self):
        data = self.data.copy()
        del data['type']
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        try:
            wh_mapper_models.SystemNode.objects.get(**data)
            raise self.failureException('System node object was created')
        except:
            pass

    def test_create_node_missing_page(self):
        data = self.data.copy()
        del data['page_name']
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        try:
            wh_mapper_models.SystemNode.objects.get(**data)
            raise self.failureException('System node object was created')
        except:
            pass

    def test_create_node_invalid_name(self):
        data = self.data.copy()
        data['name'] = '         '
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        try:
            wh_mapper_models.SystemNode.objects.get(**data)
            raise self.failureException('System node object was created')
        except:
            pass

    def test_create_node_invalid_type(self):
        data = self.data.copy()
        data['type'] = 'invalid type'
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        try:
            wh_mapper_models.SystemNode.objects.get(**data)
            raise self.failureException('System node object was created')
        except:
            pass

    def test_create_node_invalid_parent(self):
        data = self.data.copy()
        data['parent_node'] = 'invalid parent'
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        try:
            wh_mapper_models.SystemNode.objects.get(**data)
            raise self.failureException('System node object was created')
        except:
            pass


class SystemNodeDeleteAPITestCase(TestCase):
    url = '/api/system_node/'

    def test_delete_root_node(self):
        util = SystemNodeTestUtilities()
        test_root_node_id = util.create_test_root_node()
        response = self.client.delete(self.url + test_root_node_id + '/')
        self.assertEqual(response.status_code, 200)
        try:
            wh_mapper_models.SystemNode.objects.get(id=test_root_node_id)
            raise self.failureException('System node object was not deleted')
        except:
            pass

    def test_delete_node_chain(self):
        util = SystemNodeTestUtilities()
        test_root_node_id = util.create_test_root_node()
        node = wh_mapper_models.SystemNode.objects.get(id=test_root_node_id)

        node_id_list = []
        for i in range(5):
            node.parent_node_id = node.id
            node.id = ''
            node.date = ''
            node.save()
            node_id_list.append(node.id)

        response = self.client.delete(self.url + node_id_list[0] + '/')
        self.assertEqual(response.status_code, 200)
        if wh_mapper_models.SystemNode.objects.filter(id__in=node_id_list):
            raise self.failureException('System node objects were not deleted')

    def test_delete_node_invalid_id(self):
        response = self.client.delete(self.url + 'invalid id' + '/')
        self.assertEqual(response.status_code, 400)
