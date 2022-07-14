from django.db import models

from base import abstract_models


class Lesson(abstract_models.AbstractBaseName,
             abstract_models.IsActive,
             abstract_models.Ordering,
             abstract_models.TimeStampedModel):
    icon = models.ImageField(upload_to='lesson')

    class Meta:
        db_table = 'quiz\".\"lesson'

    def __str__(self):
        return f"{self.name_ru}"
