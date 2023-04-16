from django.db import models

from base import abstract_models


class Speciality(abstract_models.AbstractBaseName,
                 abstract_models.AbstractBaseNameCode,
                 abstract_models.IsActive,
                 abstract_models.Ordering,
                 abstract_models.TimeStampedModel):
    icon = models.FileField(upload_to='university')
    short_name_kz = models.CharField(max_length=255, null=True)
    short_name_ru = models.CharField(max_length=255, null=True)
    short_name_en = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    description_kz = models.TextField(null=True)
    description_en = models.TextField(null=True)
    description_ru = models.TextField(null=True)
    min_bal = models.IntegerField(default=0)
    min_bal_with_quota = models.IntegerField(default=0)
    avg_cost = models.IntegerField(default=0)
    avg_salary = models.IntegerField(default=0)

    class Meta:
        db_table = 'universities\".\"speciality'

    def __str__(self):
        return f' {self.name_ru}'
