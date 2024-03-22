from io import BytesIO
from unittest.mock import patch
import requests
import requests_mock
from PIL import Image
from rest_framework.test import APITestCase

from region.models import Sigungu

class FacilityGetAPITestCase(APITestCase):
    fixtures = ["init_data.json", "test_data.json"]

    def test_facility_list(self):
        response = self.client.get("/api/facilities/")
        self.assertEqual(response.status_code, 200)

    def test_facility_detail(self):
        response = self.client.get("/api/facilities/0ac8df28-ad6d-4a8d-aef6-28a71a702fec/")
        self.assertEqual(response.status_code, 200)

def generate_photo_file():
    file = BytesIO()
    image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
    image.save(file, "png")
    file.name = "test.png"
    file.seek(0)
    return file

class FacilityCreateAPITestCase(APITestCase):
    fixtures = ["init_data.json", "test_data.json"]

    def setUp(self):
        self.url = "/api/facilities/"
        self.data = {
            "name": "테스트 시설",
            "member_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "member_name": "테스트",
            "member_phone": "010-1234-5678",
            "reg_code": "012-01-01234",
            "phone": "010-1234-5678",
            "road_address_part1": "서울특별시",
            "road_address_part2": "강남구",
            "building_name": "테스트 빌딩",
            "zip_code": "12345",
        }

    @requests_mock.Mocker()
    def test_facility_create_success(self, m):
        with patch("facility.views.get_coordinates") as mock_get_coordinates, \
             patch('django.core.files.storage.default_storage.save') as mock_save:
            self.data["bcode"] = "1111000000"

            mock_get_coordinates.return_value = (
                37.123456, 127.123456,
                "경기도 용인", "Yongin, Gyeonggi-do"
            )
            m.get(
                'https://naveropenapi.apigw.ntruss.com/map-static/v2/raster',
                content=generate_photo_file().getvalue(),
                status_code=200
            )
            mock_save.return_value = 'test.png'
            response = self.client.post(self.url, self.data)
            self.assertEqual(response.status_code, 201)

    def test_facility_create_failure_existing_regcode(self):
        with patch("facility.views.get_coordinates") as mock_get_coordinates, \
             patch("facility.views.fetch_map_image") as mock_fetch_map_image, \
             patch("django.core.files.storage.default_storage.save") as mock_save:
            mock_get_coordinates.return_value = (
                37.123456, 127.123456,
                "경기도 용인", "Yongin, Gyeonggi-do"
            )
            mock_fetch_map_image.return_value = generate_photo_file()
            mock_save.return_value = "test.png"
            self.data["bcode"] = "1111000000"
            self.data["reg_code"] = "987-65-43210"
            response = self.client.post(self.url, self.data)
            self.assertEqual(response.status_code, 400)

    @requests_mock.Mocker()
    def test_facility_create_failure_bcode(self, m):
        m.get(
            'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode',
            json={
                "addresses": [{
                    "jibunAddress": "경기도 용인시",
                    "englishAddress": "Yongin, Gyeonggi-do",
                    "x": "127.123456",
                    "y": "37.123456"
                }]
            },
            status_code=200
        )
        # 1. no bcode
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)

        # 2. wrong bcode
        self.data["bcode"] = "0000000000"
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)

        # 3. invalid bcode
        self.data["bcode"] = "asdfasdfas"
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)

    @requests_mock.Mocker()
    def test_facility_create_failure_empty_fields(self, m):
        m.get(
            'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode',
            json={
                "addresses": [{
                    "jibunAddress": "경기도 용인시",
                    "englishAddress": "Yongin, Gyeonggi-do",
                    "x": "127.123456",
                    "y": "37.123456"
                }]
            },
            status_code=200
        )
        # 1. no name
        self.data["bcode"] = "1111000000"
        del self.data["name"]
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)

        # 2. no phone
        self.data["name"] = "테스트 시설"
        del self.data["phone"]
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)

        # 3. no reg_code
        self.data["phone"] = "010-1234-5678"
        del self.data["reg_code"]
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)

        # 4. wrong reg_code
        self.data["reg_code"] = "0123456789"
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)

        # 5. no road_address_part1
        self.data["reg_code"] = "012-01-01234"
        del self.data["road_address_part1"]
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)

    @requests_mock.Mocker()
    def test_facility_create_failure_gateway(self, m):
        m.get(
            'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode',
            exc=requests.RequestException
        )
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 502)

class FacilityInfoCreateAPITestCase(APITestCase):
    fixtures = ["init_data.json", "test_data.json"]

    def setUp(self):
        convience = ["Wi-Fi", "정수기 / 냉온수기", "주차가능 (무료)", "주차가능 (유료)", "휴게공간",
                     "남녀화장실 구분", "에어컨", "난방", "락커", "탈의실", "샤워실", "사우나", "금연시설",
                     "흡연실", "어린이 놀이시설", "노키즈존", "자판기", "프로샵"]
        equipment = ["나무배트", "알루미늄배트", "글러브 대여", "포수장비 대여", "피칭머신", "배팅티",
                     "헬멧 대여", "스피드건",   "영상분석", "모니터", "스피커", "헬스기구"]
        others = [ "단체 수업 가능", "개인 코치 영업 가능", "스파이크 착용 가능", "야외 시설", "반려동물 출입가능", "휠체어 출입가능"]
        self.url = "/api/facilities/"
        self.uuid = "dd8a7793-139f-4e0a-856a-fd014ced3281"
        self.existing = "70c6826a-6e98-46e9-a876-ff5d734b03d1"
        self.info_data_full = {
            "intro": "테스트 시설 소개",
            "weekday_open": "09:00",
            "weekday_close": "18:00",
            "saturday_open": "09:00",
            "saturday_close": "18:00",
            "sunday_open": "09:00",
            "sunday_close": "18:00",
            "num_mounds": 1,
            "num_plates": 1,
            "convenience": convience,
            "equipment": equipment,
            "others": others,
            "custom": ["asdf", "fdsa"],
            "images": [generate_photo_file()],
        }
        self.info_data_blank = {
            "intro": "테스트 시설 소개",
            "weekday_open": "09:00",
            "weekday_close": "18:00",
            "saturday_open": "09:00",
            "saturday_close": "18:00",
            "sunday_open": "09:00",
            "sunday_close": "18:00",
            "num_mounds": 1,
            "num_plates": 1,
            "convenience": [],
            "equipment": [],
            "others": [],
            "custom": [],
            "images": [generate_photo_file()],
        }
        self.jongnogu = Sigungu.objects.get(sigungu_code="1111000000")

    @patch("django.core.files.storage.default_storage.save")
    def test_facility_info_create_success_full(self, mock_save):
        info_url = f"/api/facilities/{self.uuid}/info/"
        mock_save.return_value = "test.png"

        response = self.client.post(info_url, self.info_data_full, format="multipart")
        self.assertEqual(response.status_code, 201)

    @patch("django.core.files.storage.default_storage.save")
    def test_facility_info_create_success_empty(self, mock_save):
        info_url = f"/api/facilities/{self.uuid}/info/"
        mock_save.return_value = "test.png"

        response = self.client.post(info_url, self.info_data_blank, format="multipart")
        self.assertEqual(response.status_code, 201)

    def test_facility_info_create_failure_already_exists(self):
        info_url = f"/api/facilities/{self.existing}/info/"

        response = self.client.post(info_url, self.info_data_full, format="multipart")
        self.assertEqual(response.status_code, 400)

    def test_facility_info_create_failure(self):
        info_url = f"/api/facilities/{self.uuid}/info/"

        # 1. no num mounds
        del self.info_data_blank["num_mounds"]
        response = self.client.post(info_url, self.info_data_blank, format="multipart")
        self.assertEqual(response.status_code, 400)

        # 2. no num plates
        self.info_data_blank["num_mounds"] = 1
        del self.info_data_blank["num_plates"]
        self.client.post(info_url, self.info_data_blank, format="multipart")

        # 3. no intro
        self.info_data_blank["num_plates"] = 1
        del self.info_data_blank["intro"]
        self.client.post(info_url, self.info_data_blank, format="multipart")

        # 4. wrong time formats
        self.info_data_blank["intro"] = "테스트 시설 소개"
        self.info_data_blank["weekday_open"] = "0900"
        self.client.post(info_url, self.info_data_blank, format="multipart")

        self.info_data_blank["weekday_open"] = "09:00"
        self.info_data_blank["weekday_close"] = "1800"
        self.client.post(info_url, self.info_data_blank, format="multipart")

        self.info_data_blank["weekday_close"] = "18:00"
        self.info_data_blank["saturday_open"] = "0900"
        self.client.post(info_url, self.info_data_blank, format="multipart")

        self.info_data_blank["saturday_open"] = "09:00"
        self.info_data_blank["saturday_close"] = "1800"
        self.client.post(info_url, self.info_data_blank, format="multipart")

        self.info_data_blank["saturday_close"] = "18:00"
        self.info_data_blank["sunday_open"] = "0900"
        self.client.post(info_url, self.info_data_blank, format="multipart")

        self.info_data_blank["sunday_open"] = "09:00"
        self.info_data_blank["sunday_close"] = "1800"
        self.client.post(info_url, self.info_data_blank, format="multipart")

        # 5. no images
        self.info_data_blank["sunday_close"] = "18:00"
        self.info_data_blank["images"] = []
        self.client.post(info_url, self.info_data_blank, format="multipart")

class FacilityStatusCheckAPITestCase(APITestCase):
    fixtures = ["init_data.json", "test_data.json"]

    def setUp(self):
        self.uuid_step0 = "0ac8df28-ad6d-4a8d-aef6-28a71a702fec"
        self.uuid_step1 = "7d7d2817-253c-485e-8081-b20a034c44ab"
        self.url = "/api/facilities/status/"

    def test_facility_status_check_success(self):
        response = self.client.get(self.url, {"uuid": self.uuid_step0})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.url, {"uuid": self.uuid_step1})
        self.assertEqual(response.status_code, 200)

    def test_facility_status_check_failure_invalid_uuid(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

        response = self.client.get(self.url, {"uuid": "invalid"})
        self.assertEqual(response.status_code, 400)
