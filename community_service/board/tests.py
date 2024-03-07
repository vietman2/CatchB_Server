import uuid
from rest_framework.test import APITestCase

class ForumTestCase(APITestCase):
    def setUp(self):
        self.url = "/api/forums/"

    def placeholder(self):
        self.assertEqual(1, 1)
