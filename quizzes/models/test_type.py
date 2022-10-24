from django.db import models

from base import abstract_models


class TestType(abstract_models.AbstractBaseName,
               abstract_models.IsActive,
               abstract_models.Ordering,
               abstract_models.TimeStampedModel):
    code = models.CharField(max_length=125, null=True, db_index=True)
    icon = models.ImageField(upload_to='test_type', null=True, blank=True)

    class Meta:
        db_table = 'quiz\".\"test_type'
        ordering = ('order',)

    def __str__(self):
        return f"{self.name_ru}"
