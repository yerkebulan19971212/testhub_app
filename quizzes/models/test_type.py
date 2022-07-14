from django.db import models

from base import abstract_models


class TestType(abstract_models.AbstractBaseName,
               abstract_models.IsActive,
               abstract_models.Ordering,
               abstract_models.TimeStampedModel):
    icon = models.ImageField(upload_to='test_type')

    class Meta:
        db_table = 'quiz\".\"test_type'

    def __str__(self):
        return f"{self.name_ru}"
