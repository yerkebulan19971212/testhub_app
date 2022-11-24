from django.db import models

from base import abstract_models


class Variant(abstract_models.IsActive,
              abstract_models.Ordering,
              abstract_models.TimeStampedModel):
    variant = models.IntegerField()
    variant_group = models.ForeignKey(
        'quizzes.VariantGroup',
        on_delete=models.CASCADE,
        null=True,
        db_index=True,
        related_name='variants'
    )
    sum_question = models.IntegerField(default=0)
    main = models.BooleanField(default=False)

    class Meta:
        db_table = 'quiz\".\"variant'

    def __str__(self):
        return f'Вариант - {self.variant}'
