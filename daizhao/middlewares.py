from utils.identify import get_request_identify, set_response_identify
from utils.custom_random import get_compress_uuid


class SetIdentifyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        if not get_request_identify(request):
            identify = get_compress_uuid()
            set_response_identify(response, identify)

        # Code to be executed for each request/response after
        # the view is called.

        return response
