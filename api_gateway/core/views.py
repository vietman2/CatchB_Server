import requests
from rest_framework import status
from rest_framework.response import Response

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
