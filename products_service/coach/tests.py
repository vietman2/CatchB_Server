from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

class CoachGetAPITestCase(APITestCase):
    fixtures = ["init_data.json", "test_data.json"]

    def test_coach_list(self):
        response = self.client.get("/api/coaches/")
        self.assertEqual(response.status_code, 200)

    def test_coach_detail(self):
        response = self.client.get("/api/coaches/7e1186bf-3172-41df-91fd-a9f74f2508ca/")
        self.assertEqual(response.status_code, 200)

class CoachCreateAPITestCase(APITestCase):
    fixtures = ["init_data.json"]

    def setUp(self):
        self.url = "/api/coaches/"
        self.data = {
            "member_uuid": "e8217f3c-1aee-4a24-9fe6-a1347b278c16",
            "member_name": "홍길동",
            "member_phone": "010-1234-5678",
            "baseball_career": "고등학교 선수 출신",
        }

    @patch("django.core.files.storage.default_storage.save")
    def test_coach_create_pdf(self, mock_save):
        mock_save.return_value = "test.png"
        self.data["certification"] = SimpleUploadedFile(
            "test.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        response = self.client.post(self.url, self.data, format="multipart")
        self.assertEqual(response.status_code, 201)

    @patch("django.core.files.storage.default_storage.save")
    def test_coach_create_png(self, mock_save):
        mock_save.return_value = "test.png"
        self.data["certification"] = SimpleUploadedFile(
            "test.png",
            b"file_content",
            content_type="image/png"
        )
        response = self.client.post(self.url, self.data, format="multipart")
        self.assertEqual(response.status_code, 201)

    @patch("django.core.files.storage.default_storage.save")
    def test_coach_create_jpeg(self, mock_save):
        mock_save.return_value = "test.png"
        self.data["certification"] = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        response = self.client.post(self.url, self.data, format="multipart")
        self.assertEqual(response.status_code, 201)

    def test_coach_create_invalid_certification(self):
        self.data["certification"] = SimpleUploadedFile(
            "test.txt",
            b"file_content",
            content_type="text/plain"
        )
        response = self.client.post(self.url, self.data, format="multipart")
        self.assertEqual(response.status_code, 400)

    def test_coach_create_invalid_career(self):
        self.data["baseball_career"] = "선수 출신"
        response = self.client.post(self.url, self.data, format="multipart")
        self.assertEqual(response.status_code, 400)

class CoachInfoCreateAPITestCase(APITestCase):
    fixtures = ["init_data.json", "test_data.json"]

    def setUp(self):
        self.uuid = "c5c5636e-74e8-4ee5-b0d8-8356830b2e76"
        self.url = f"/api/coaches/{self.uuid}/info/"
        self.data = {
            "intro": "투수로서의 경험을 공유합니다.",
            "regions": [1111000000],
            "specialty": ["투구", "타격", "수비", "포수수비", "재활", "컨디셔닝"],
            "level": ["비기너1", "비기너2", "아마추어", "베테랑", "루키", "엘리트"],
            "lesson_type": ["개인 레슨", "소그룹 레슨", "팀 레슨", "기타"],
            "images": [
                SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg"),
                SimpleUploadedFile("test.png", b"file_content", content_type="image/png")
            ],
        }
        self.data_empty = {
            "intro": "투수로서의 경험을 공유합니다.",
            "regions": [1111000000],
        }

    @patch("django.core.files.storage.default_storage.save")
    def test_coach_info_create(self, mock_save):
        mock_save.return_value = "test.png"
        response = self.client.post(self.url, self.data, format="multipart")
        self.assertEqual(response.status_code, 201)

    @patch("django.core.files.storage.default_storage.save")
    def test_coach_info_create_empty(self, mock_save):
        mock_save.return_value = "test.png"
        response = self.client.post(self.url, self.data_empty, format="multipart")
        self.assertEqual(response.status_code, 201)

    @patch("django.core.files.storage.default_storage.save")
    def test_coach_info_create_existing(self, mock_save):
        mock_save.return_value = "test.png"
        response = self.client.post(self.url, self.data, format="multipart")
        response = self.client.post(self.url, self.data, format="multipart")
        self.assertEqual(response.status_code, 400)

class CoachStatusCheckAPITestCase(APITestCase):
    fixtures = ["init_data.json", "test_data.json"]

    def setUp(self):
        self.url = "/api/coaches/status/"
        self.uuid_step0 = "7e1186bf-3172-41df-91fd-a9f74f2508ca"
        self.uuid_step1 = "cc8eb907-97fa-42b1-9b74-4126b04bc024"

    def test_coach_status_check(self):
        response = self.client.get(self.url, {"uuid": self.uuid_step0})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.url, {"uuid": self.uuid_step1})
        self.assertEqual(response.status_code, 200)

    def test_coach_status_check_invalid_uuid(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

        response = self.client.get(self.url, {"uuid": "invalid"})
        self.assertEqual(response.status_code, 400)
