from rest_framework.exceptions import *  # noqa
# from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class DoesNotExist(APIException):
    status_code = 1000
    default_detail = _('Authentication credentials were not provided.')
    default_code = 'not_authenticated'


class UnexpectedError(APIException):
    status_code = 1001
    default_detail = _('Authentication credentials were not provided.')
    default_code = 'not_authenticated'
