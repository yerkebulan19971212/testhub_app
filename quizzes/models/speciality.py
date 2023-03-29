from django.db import models

from base import abstract_models


class Speciality(abstract_models.AbstractBaseName,
              abstract_models.AbstractBaseNameCode,
              abstract_models.IsActive,
              abstract_models.Ordering,
              abstract_models.TimeStampedModel):
    icon = models.FileField(upload_to='university')
    short_name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()


    class Meta:
        db_table = 'quiz\".\"university'

    def __str__(self):
        return f' {self.name_ru}'
