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

        return lat, lng

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
        if request.data['address']['road_address_part1'] == '':
            return Response(
                {'message': '주소를 입력해주세요.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        REQUEST_URL = f'{products_service_url}/api/facilities/'

        body = request.body

        address = request.data['address']['road_address_part1']
        lat, lng = get_coordinates(address)

        return get_response(request.headers, body, REQUEST_URL, 'POST', {'lat': lat, 'lng': lng})
