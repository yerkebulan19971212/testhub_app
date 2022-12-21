from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class MainException(APIException):
    exception_status_code = 0


class UnexpectedError(MainException):
    status_code = 200
    exception_status_code = 1001
    default_detail = "Unexpected error"
    default_code = "unexpected_error"


class DoesNotExist(MainException):
    status_code = 200
    exception_status_code = 2001
    default_detail = _('Does not exist in db.')
    default_code = 'does_not_exist'
