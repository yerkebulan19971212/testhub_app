from django.db import models

from base import abstract_models


class University(abstract_models.AbstractBaseName,
              abstract_models.AbstractBaseNameCode,
              abstract_models.IsActive,
              abstract_models.Ordering,
              abstract_models.TimeStampedModel):
    icon = models.FileField(upload_to='university')
    short_name = models.CharField(max_length=255)


    class Meta:
        db_table = 'quiz\".\"university'

    def __str__(self):
        return f' {self.name_ru}'
