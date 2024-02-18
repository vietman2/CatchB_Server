import json
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

products_service_url = settings.SERVICE_URLS['products_service']

def get_coordinates(address):
    naver_geocode_url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode'
    headers = {
        'X-NCP-APIGW-API-KEY-ID': settings.NAVER_CLIENT_ID,
        'X-NCP-APIGW-API-KEY': settings.NAVER_CLIENT_SECRET,
        'Accept': 'application/json',
    }
    params = {
        'query': address,
    }

    try:
        response = requests.request(
                method='GET',
                url=naver_geocode_url,
                headers=headers,
                params=params,
                timeout=10,
            )

        lat = response.json()['addresses'][0]['y']
        lng = response.json()['addresses'][0]['x']
        jibun_address = response.json()['addresses'][0]['jibunAddress']
        english_address = response.json()['addresses'][0]['englishAddress']

        return lat, lng, jibun_address, english_address

    except requests.RequestException as e:
        return Response(
            {'message': str(e)},
            status=status.HTTP_502_BAD_GATEWAY,
        )

def get_response(headers, body, url, method, query_params=None):
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=body,
            params=query_params,
            timeout=10,
        )

        return Response(
            response.json(),
            status=response.status_code,
        )

    except requests.RequestException as e:
        return Response(
            {'message': str(e)},
            status=status.HTTP_502_BAD_GATEWAY,
        )

class FacilityView(APIView):
    def post(self, request):
        original_body = json.loads(request.body.decode('utf-8'))

        if request.data['road_address_part1'] is "":
            return Response(
                {'message': '주소를 입력해주세요.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.data['road_address_part2'] is "":
            return Response(
                {'message': '상세 주소를 입력해주세요.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        query = request.data['road_address_part1']
        lat, lng, jibun_address, english_address = get_coordinates(query)

        modified_data = original_body

        modified_data['latitude'] = lat
        modified_data['longitude'] = lng
        modified_data['jibun_address'] = jibun_address
        modified_data['eng_address'] = english_address

        REQUEST_URL = f'{products_service_url}/api/facilities/'

        modified_body = json.dumps(modified_data)

        return get_response(
            request.headers,
            modified_body,
            REQUEST_URL,
            'POST'
        )
