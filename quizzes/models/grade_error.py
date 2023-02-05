from django.db import models

from base import abstract_models
from base.constant import ErrorType


class InfoError(abstract_models.TimeStampedModel,
                 abstract_models.IsActive):
    error_name = models.TextField()
    error_type = models.IntegerField(choices=ErrorType.choices())

    class Meta:
        db_table = 'info\".\"info_error'
