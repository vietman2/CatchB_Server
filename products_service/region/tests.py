from rest_framework.test import APITestCase

class RegionAPITestCase(APITestCase):
    def setUp(self):
        self.url = "/api/regions/"

    def test_unallowed_methods(self):
        response = self.client.get(f"{self.url}1/")
        self.assertEqual(response.status_code, 405)

    def test_sido_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
