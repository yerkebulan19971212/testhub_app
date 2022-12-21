from django.http import Http404
from rest_framework import status, exceptions
from rest_framework.exceptions import PermissionDenied
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import set_rollback, exception_handler

from base.exceptions import MainException, UnexpectedError


class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            "status": True,
            "status_code": status_code,
            "result": data,
            "message": None
        }
        if not str(status_code).startswith('2'):
            response["status"] = False
            response["data"] = None
            try:
                response["message"] = data["detail"]
            except KeyError:
                response["data"] = data

        return super().render(response, accepted_media_type, renderer_context)


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

    if isinstance(exc, MainException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}
        response = {
            "status": False,
            "status_code": exc.exception_status_code,
            "result": None,
            "message": exc.detail
        }
        set_rollback()
        return Response(response, status=status.HTTP_200_OK, headers=headers)

    return None


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        response = exception_handler(UnexpectedError(), context)
        set_rollback()
    return response
