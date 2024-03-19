from io import BytesIO
from unittest.mock import patch
from PIL import Image
from rest_framework.test import APITestCase

from region.models import Sido, Sigungu
from .models import FacilityInfo

class FacilityAPITestCase(APITestCase):
    def generate_photo_file(self):
        file = BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.name = "test.png"
        file.seek(0)
        return file

    def setUp(self):
        convience = ["Wi-Fi", "정수기 / 냉온수기", "주차가능 (무료)", "주차가능 (유료)", "휴게공간",
                     "남녀화장실 구분", "에어컨", "난방", "락커", "탈의실", "샤워실", "사우나", "금연시설",
                     "흡연실", "어린이 놀이시설", "노키즈존", "자판기", "프로샵"]
        equipment = ["나무배트", "알루미늄배트", "글러브 대여", "포수장비 대여", "피칭머신", "배팅티",
                     "헬멧 대여", "스피드건",   "영상분석", "모니터", "스피커", "헬스기구"]
        others = [ "단체 수업 가능", "개인 코치 영업 가능", "스파이크 착용 가능", "야외 시설", "반려동물 출입가능", "휠체어 출입가능"]
        self.url = "/api/facilities/"
        self.data = {
            "name": "테스트 시설",
            "member_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "member_name": "테스트",
            "member_phone": "010-1234-5678",
            "reg_code": "012-34-56789",
            "phone": "010-1234-5678",
            "road_address_part1": "서울특별시",
            "road_address_part2": "강남구",
            "building_name": "테스트 빌딩",
            "zip_code": "12345",
        }
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
            #"custom": ["asdf", "fdsa"],
            #"images": [self.generate_photo_file()],
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
            #"images": [self.generate_photo_file()],
        }
        sido1 = Sido.objects.create(
            sido_code=1100000000, sido_name="서울특별시", label="서울", display="서울시"
        )
        self.sigungu1 = Sigungu.objects.create(
            sigungu_code=1111000000, sigungu_name="종로구", sido=sido1
        )

    def test_facility_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_facility_create_success(self):
        with patch("facility.views.get_coordinates") as mock_get_coordinates, \
             patch("facility.views.fetch_map_image") as mock_fetch_map_image, \
             patch('django.core.files.storage.default_storage.save') as mock_save, \
             patch("region.models.SigunguManager.get_sigungu_from_bcode") as mock_get_sigungu:
            self.data["bcode"] = "1111000000"

            mock_get_coordinates.return_value = (37.123456, 127.123456, "경기도 용인", "Yongin, Gyeonggi-do")
            mock_fetch_map_image.return_value = self.generate_photo_file()
            mock_save.return_value = 'test.png'
            mock_get_sigungu.return_value = self.sigungu1
            response = self.client.post(self.url, self.data)
            self.assertEqual(response.status_code, 201)

    def test_facility_create_failure(self):
        with patch("facility.views.get_coordinates") as mock:
            mock.return_value = (37.123456, 127.123456, "경기도 용인", "Yongin, Gyeonggi-do")
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

            # 4. no name
            self.data["bcode"] = "1111000000"
            del self.data["name"]
            response = self.client.post(self.url, self.data)
            self.assertEqual(response.status_code, 400)

            # 5. no phone
            self.data["name"] = "테스트 시설"
            del self.data["phone"]
            response = self.client.post(self.url, self.data)
            self.assertEqual(response.status_code, 400)

            # 6. no reg_code
            self.data["phone"] = "010-1234-5678"
            del self.data["reg_code"]
            response = self.client.post(self.url, self.data)
            self.assertEqual(response.status_code, 400)

            # 7. wrong reg_code
            self.data["reg_code"] = "0123456789"
            response = self.client.post(self.url, self.data)
            self.assertEqual(response.status_code, 400)

    def test_facility_info_create_success_full(self):
        with patch("facility.views.get_coordinates") as mock_get_coordinates, \
             patch("facility.views.fetch_map_image") as mock_fetch_map_image, \
             patch('django.core.files.storage.default_storage.save') as mock_save, \
             patch("region.models.SigunguManager.get_sigungu_from_bcode") as mock_get_sigungu:

            self.data["bcode"] = "1111000000"

            mock_get_coordinates.return_value = (37.123456, 127.123456, "경기도 용인", "Yongin, Gyeonggi-do")
            mock_fetch_map_image.return_value = self.generate_photo_file()
            mock_save.return_value = 'test.png'
            mock_get_sigungu.return_value = self.sigungu1
            response = self.client.post(self.url, self.data)
            self.assertEqual(response.status_code, 201)

            facility_uuid = response.data["uuid"]
            info_url = f"/api/facilities/{facility_uuid}/info/"

            response = self.client.post(info_url, self.info_data_full, format="multipart")
            self.assertEqual(response.status_code, 201)

            FacilityInfo.objects.get().delete()

            response = self.client.post(info_url, self.info_data_blank, format="multipart")
            self.assertEqual(response.status_code, 201)

    def test_facility_info_create_failure_already_exists(self):
        with patch("facility.views.get_coordinates") as mock_get_coordinates, \
             patch("facility.views.fetch_map_image") as mock_fetch_map_image, \
             patch('django.core.files.storage.default_storage.save') as mock_save, \
             patch("region.models.SigunguManager.get_sigungu_from_bcode") as mock_get_sigungu:
            mock_get_coordinates.return_value = (0, 0, "asdf", "asdf")
            mock_fetch_map_image.return_value = self.generate_photo_file()
            mock_save.return_value = 'test.png'
            mock_get_sigungu.return_value = self.sigungu1

            self.data["bcode"] = "1111000000"
            response = self.client.post(self.url, self.data)
            self.assertEqual(response.status_code, 201)

            facility_uuid = response.data["uuid"]
            info_url = f"/api/facilities/{facility_uuid}/info/"

            response = self.client.post(info_url, self.info_data_full, format="multipart")
            self.assertEqual(response.status_code, 201)

            response = self.client.post(info_url, self.info_data_full, format="multipart")
            self.assertEqual(response.status_code, 400)

    def test_facility_info_create_failure(self):
        with patch("facility.views.get_coordinates") as mock_get_coordinates, \
             patch("facility.views.fetch_map_image") as mock_fetch_map_image, \
             patch('django.core.files.storage.default_storage.save') as mock_save, \
             patch("region.models.SigunguManager.get_sigungu_from_bcode") as mock_get_sigungu:
            mock_get_coordinates.return_value = (0, 0, "asdf", "asdf")
            mock_fetch_map_image.return_value = self.generate_photo_file()
            mock_save.return_value = 'test.png'
            mock_get_sigungu.return_value = self.sigungu1

            mock_get_coordinates.return_value = (0, 0, "asdf", "asdf")
            self.data["bcode"] = "1111000000"
            response = self.client.post(self.url, self.data)

            facility_uuid = response.data["uuid"]
            info_url = f"/api/facilities/{facility_uuid}/info/"

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
