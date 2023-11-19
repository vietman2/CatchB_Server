from django.conf import settings

def service(url):
    if "/calendar" in url:
        return settings.SERVICE_URLS['calendar_service']
    if "/community" in url:
        return settings.SERVICE_URLS['community_service']
    if "/payments" in url:
        return settings.SERVICE_URLS['payments_service']
    if "/products" in url:
        return settings.SERVICE_URLS['products_service']
    if "/user_management" in url:
        return settings.SERVICE_URLS['user_management_service']

    return None

def router(request):
    request_url = request.path
    #request_method = request.method
    #request_headers = request.headers
    #request_body = request.body

    #service_url = service(request_url)
    service(request_url)
