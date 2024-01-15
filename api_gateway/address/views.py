import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class AddressView(APIView):
    def split_data(self, json_data):
        sido = []
        sigungu = []
        sigungu_by_sido = {'세종특별자치시': ['세종특별자치시']}
        exceptions = ['경기도 수원시', '경기도 성남시', '경기도 안양시', '경기도 안산시', '경기도 고양시', '경기도 용인시',
                      '충청북도 청주시', '충청남도 천안시', '전라북도 전주시', '경상북도 포항시', '경상남도 창원시']

        for data in json_data:
            if data['code'][-8:] == '00000000':
                sido.append(data)
                sigungu_by_sido[data['name']] = []
            else:
                sigungu.append(data)
                if ' ' not in data['name']:
                    continue
                if data['name'] in exceptions:
                    continue

                sido_name = data['name'].split(' ', 1)[0]
                sigungu_by_sido[sido_name].append(data['name'].split(' ', 1)[1])

        sido.append({'code': '3611000000', 'name': '세종특별자치시'})
        sigungu.append({'code': '3611000000', 'name': '세종특별자치시'})

        return sido, sigungu, sigungu_by_sido

    def get(self, request): # pylint: disable=W0613
        base_url = 'https://grpc-proxy-server-mkvo6j4wsq-du.a.run.app/v1/regcodes'
        url2 = base_url + '?regcode_pattern=*00000'

        try:
            response = requests.request(
                method='GET',
                url=url2,
                timeout=10,
            )

            sido, sigungu, sigungu_by_sido = self.split_data(response.json()['regcodes'])

            return Response(
                data={
                    'sido': sido,
                    'sigungu': sigungu,
                    'sigungu_by_sido': sigungu_by_sido,
                },
                status=status.HTTP_200_OK,
            )

        except requests.RequestException as e:
            return Response(
                {'message': str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )
