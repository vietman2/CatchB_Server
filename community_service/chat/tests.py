import uuid
from rest_framework.test import APITestCase

from .models import ChatRoom

class ChatRoomAPITestCase(APITestCase):
    def setUp(self):
        self.url = '/api/chatroom/'
        self.user_uuid = uuid.uuid4()
        self.other_uuid = uuid.uuid4()
        self.other2_uuid = uuid.uuid4()
        self.data = {
            'members': [
                {
                    'user_uuid': self.user_uuid,
                    'user_name': 'user1',
                },
                {
                    'user_uuid': self.other_uuid,
                    'user_name': 'user2',
                }
            ]
        }
        self.data2 = {
            'members': [
                {
                    'user_uuid': self.user_uuid,
                    'user_name': 'user1',
                },
                {
                    'user_uuid': self.other2_uuid,
                    'user_name': 'user3',
                }
            ]
        }
        self.data3 = {
            'members': [
                {
                    'user_uuid': self.other_uuid,
                    'user_name': 'user2',
                },
                {
                    'user_uuid': self.other2_uuid,
                    'user_name': 'user3',
                }
            ]
        }
        self.updated_data = {
            'members': [self.user_uuid,self.other_uuid],
            'name': 'new name'
        }

    def test_chatroom_apis(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 201)
        # check if it is saved in db
        chatroom = ChatRoom.objects.get(id=response.data['id'])
        self.assertEqual(chatroom.members.count(), 2)
        self.assertEqual(ChatRoom.objects.count(), 1)

        # test duplicate creation: should return 400
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 400)

        # create 2 more and test list
        self.client.post(self.url, self.data2, format='json')
        self.client.post(self.url, self.data3, format='json')
        response = self.client.get(self.url, {
            'user_uuid': self.user_uuid
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        # test retrieve
        response = self.client.get(self.url + f'{chatroom.id}/', {
            'user_uuid': self.user_uuid
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], chatroom.id)
        self.assertEqual(response.data['members'][0], self.user_uuid)
        self.assertEqual(response.data['members'][1], self.other_uuid)
        self.assertEqual(response.data['name'], 'user2')

        # test update
        response = self.client.put(self.url + f'{chatroom.id}/?user_uuid={self.user_uuid}', data=self.updated_data, format='json')
        self.assertEqual(response.status_code, 200)

        # test delete
        response = self.client.delete(self.url + f'{chatroom.id}/?user_uuid={self.user_uuid}')
        self.assertEqual(response.status_code, 204)
        # check soft delete
        self.assertEqual(ChatRoom.objects.count(), 3)
        self.assertEqual(ChatRoom.objects.get(id=chatroom.id).left_members.count(), 1)

    def test_chatroom_apis_with_invalid_data(self):
        response = self.client.post(self.url, self.data, format='json')
        chatroom = ChatRoom.objects.get(id=response.data['id'])
        response = self.client.get(self.url + f'{chatroom.id}/')
        self.assertEqual(response.status_code, 400)

        data = {
            'members': [
                {
                    'user_uuid': self.user_uuid,
                    'user_name': 'user1',
                },
                {
                    'user_uuid': self.user_uuid,
                    'user_name': 'user2',
                }
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

        data['members'][1]['user_uuid'] = 'invalid uuid'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

        response = self.client.put(
            self.url + f'{chatroom.id}/?user_uuid={self.user_uuid}',
            data={},
            format='json'
        )
        self.assertEqual(response.status_code, 400)
