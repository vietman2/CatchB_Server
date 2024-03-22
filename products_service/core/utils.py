import requests
from django.conf import settings
from django.core.files.base import ContentFile

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

def fetch_map_image(lat, lng):
    naver_staticmap_url = 'https://naveropenapi.apigw.ntruss.com/map-static/v2/raster'
    headers = {
        'X-NCP-APIGW-API-KEY-ID': settings.NAVER_CLIENT_ID,
        'X-NCP-APIGW-API-KEY': settings.NAVER_CLIENT_SECRET,
    }
    params = {
        'center': f'{lng},{lat}',
        'level': 15,
        'w': 500,
        'h': 300,
        'format': 'png',
        'markers': f'type:d|size:small|pos:{lng} {lat}|color:0x14863e|viewSizeRatio:0.75',
    }

    response = requests.request(
            method='GET',
            url=naver_staticmap_url,
            headers=headers,
            params=params,
            timeout=10,
        )

    return ContentFile(response.content)
