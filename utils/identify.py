from django.conf import settings


def set_response_identify(res, identify):
    key = settings.IDENTIFY_KEY
    res.set_signed_cookie(key, identify, salt=settings.SECRET_KEY)
    return identify


def get_request_identify(request):
    key = settings.IDENTIFY_KEY
    if key not in request.COOKIES:
        return
    identify = request.get_signed_cookie(key, salt=settings.SECRET_KEY)
    return identify
