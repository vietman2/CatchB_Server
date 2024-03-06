from django.test import TestCase

from lesson.models import LessonProduct

class LessonTestCase(TestCase):
    def setUp(self):
        self.url = "/api/lessons/"
        self.coach_uuid = "123e4567-e89b-12d3-a456-426614174000"
        self.data = {
            "title": "테스트 레슨 상품",
            "description": "테스트 레슨 상품 설명",
            "price": 10000,
            "main_coach": self.coach_uuid,
            "num_sessions": 10,
        }
        LessonProduct.objects.create(
            title="1시간 레슨",
            description="타격 레슨",
            price=30000,
            main_coach=self.coach_uuid,
            num_sessions=1,
        )
        LessonProduct.objects.create(
            title="2시간 레슨",
            description="수비 레슨",
            price=50000,
            main_coach=self.coach_uuid,
            num_sessions=1,
        )

    def test_lesson_product(self):
        response = self.client.post(self.url, data=self.data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(LessonProduct.objects.all()), 3)
        id = response.data["id"]    #pylint: disable=W0622

        response = self.client.get(f"{self.url}{id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.data["title"])

        fix_data = {
            "title": "바뀐 레슨 상품",
        }
        response = self.client.patch(
            f"{self.url}{id}/",
            data=fix_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], fix_data["title"])

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

        response = self.client.delete(f"{self.url}{id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(LessonProduct.objects.all()), 3)
        self.assertEqual(LessonProduct.objects.get(id=id).deleted, True)

    def test_lesson_list_query(self):
        response = self.client.get(f"{self.url}?coach_uuid={self.coach_uuid}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(f"{self.url}?price=40000")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(f"{self.url}?price=100000")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_lesson_product_fail(self):
        response = self.client.post(self.url, data=self.data, format="json")
        lesson_id = response.data["id"]    #pylint: disable=W0622

        response = self.client.put(f"{self.url}{id}/", data=self.data)
        self.assertEqual(response.status_code, 405)

        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(self.url, data={"title": "테스트 레슨 상품"})
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(
            f"{self.url}{lesson_id}/",
            data={},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(
            f"{self.url}{lesson_id}/",
            data={
                "price": -1000
            },
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

        self.data["price"] = -1000
        response = self.client.post(self.url, data=self.data, format="json")
        self.assertEqual(response.status_code, 400)
