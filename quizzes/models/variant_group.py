from django.db import models

from base import abstract_models
from quizzes.models import TestType


class VariantGroup(abstract_models.AbstractBaseName,
                   abstract_models.IsActive,
                   abstract_models.Ordering,
                   abstract_models.TimeStampedModel):
    test_type = models.ForeignKey(
        TestType,
        on_delete=models.CASCADE,
        related_name='variant_groups',
        null=True,
        blank=True
    )
    duration = models.DurationField(null=True)

    class Meta:
        db_table = 'quiz\".\"variant_group'

    def __str__(self):
        return f'{self.name_kz}'
