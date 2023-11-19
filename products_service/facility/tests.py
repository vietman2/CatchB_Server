from rest_framework.test import APITestCase

class FacilityAPITestCase(APITestCase):
    def setUp(self):
        self.url = "/api/facility/"
        self.data = {
            "name": "테스트 시설",
            "image_urls": ["https://test.com/test.jpg"],
            "hashtags": ["#테스트", "#시설"],
            "description": "테스트 시설입니다.",
            "address": "서울시 강남구 테스트로 123",
            "phone": "010-1234-5678",
        }
