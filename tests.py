from django.test import TestCase

import wh_mapper.models as wh_mapper_models

class SystemNodeCreateAPITestCase(TestCase):
    url = '/api/system_node/'

    def create_test_root_node(self):
        test_root_node = wh_mapper_models.SystemNode(author='testuser',
                                                     name='Testville',
                                                     type='high',
                                                     page_name='testpage')
        test_root_node.save()
        return test_root_node.id

    def test_create_root_node(self):
        data = {'author': 'testuser', 'name': 'Testville', 'type': 'high',
                'page_name': 'testpage'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        system_node = wh_mapper_models.SystemNode.objects.get(**data)
        self.assertEqual(system_node.parent_node_id, None)

    def test_create_child_node(self):
        test_root_node_id = self.create_test_root_node()
        data = {'author': 'testuser', 'name': 'Childville', 'type': 'low',
                'page_name': 'testpage', 'parent_node': test_root_node_id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        wh_mapper_models.SystemNode.objects.get(**data)
