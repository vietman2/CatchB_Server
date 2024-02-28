from rest_framework.test import APITestCase

from account.models import Bank

class BankListAPITestCase(APITestCase):
    def test_unallowed_methods(self):
        response = self.client.post("/api/banks/")
        self.assertEqual(response.status_code, 405)

        response = self.client.put("/api/banks/")
        self.assertEqual(response.status_code, 405)

        response = self.client.patch("/api/banks/")
        self.assertEqual(response.status_code, 405)

        response = self.client.delete("/api/banks/")
        self.assertEqual(response.status_code, 405)

        response = self.client.get("/api/banks/1/")
        self.assertEqual(response.status_code, 405)

    def test_get_list(self):
        response = self.client.get("/api/banks/")
        self.assertEqual(response.status_code, 200)
