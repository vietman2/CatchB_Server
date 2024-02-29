from rest_framework.test import APITestCase

class BankListAPITestCase(APITestCase):
    def setUp(self):
        self.url = "/api/banks/"

    def test_unallowed_methods(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

        response = self.client.put(self.url + "1/")
        self.assertEqual(response.status_code, 405)

        response = self.client.patch(self.url + "1/")
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(self.url + "1/")
        self.assertEqual(response.status_code, 405)

        response = self.client.get(self.url + "1/")
        self.assertEqual(response.status_code, 405)

    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
