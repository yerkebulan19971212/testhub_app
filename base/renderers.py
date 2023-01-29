from django.http import Http404
from rest_framework import status, exceptions
from rest_framework.exceptions import PermissionDenied
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import set_rollback


class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            "status": True,
            "message": "Success",
            "status_code": 0,
            "result": data,
        }
        if not str(status_code).startswith('2'):
            response["status"] = False
            response["status_code"] = 1000
            response["result"] = None
            try:
                response["message"] = data["detail"]
            except KeyError:
                response["data"] = data

        return super().render(response, accepted_media_type, renderer_context)


# class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
#
#     def render(self, data, accepted_media_type=None, renderer_context=None):
#         status_code = renderer_context['response'].status_code
#         response = {
#             "status": "success",
#             "code": status_code,
#             "data": data,
#             "message": None
#         }
#
#         if not str(status_code).startswith('2'):
#             response["status"] = "error"
#             response["data"] = None
#             try:
#                 response["message"] = data["detail"]
#             except KeyError:
#                 response["data"] = data
#
#         return super().render(response,
#                                                   accepted_media_type,
#                                                   renderer_context)
def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

        set_rollback()
        return Response(data, status=status.HTTP_200_OK, headers=headers)

    return None


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    # to get the standard error response.
    response = exception_handler(exc, context)
    # response == None is an exception not handled by the DRF framework in the call above
    if response is not None:
        print(exc.status_code)
        print(exc)
        response.data['status_code'] = exc.status_code
    else:
        response = Response({'detail': 'Unhandled server error'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response.data['status_code'] = 500

        set_rollback()

    return response
