from rest_framework.test import APITestCase

class RegionAPITestCase(APITestCase):
    def setUp(self):
        self.url = "/api/regions/"
        
    def test_sido_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)