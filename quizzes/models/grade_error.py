from django.db import models

from base import abstract_models


class GradeError(abstract_models.TimeStampedModel,
                 abstract_models.IsActive):
    error_name = models.TextField()

    class Meta:
        db_table = 'info\".\"grade_error'
