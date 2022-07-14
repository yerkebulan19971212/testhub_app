from django.db import models

from base import abstract_models


class Variant(abstract_models.IsActive,
              abstract_models.Ordering,
              abstract_models.TimeStampedModel):
    variant = models.IntegerField()
    main = models.BooleanField(default=False)

    class Meta:
        db_table = 'quiz\".\"variant'

    def __str__(self):
        return f'Вариант - {self.variant}'
