from django.db import models

from base import abstract_models


class Lesson(abstract_models.AbstractBaseName,
             abstract_models.AbstractBaseNameCode,
             abstract_models.IsActive,
             abstract_models.Ordering,
             abstract_models.TimeStampedModel):
    icon = models.FileField(upload_to='lesson', null=True, blank=True)
    chosen_icon = models.FileField(upload_to='lesson', null=True, blank=True)
    math = models.BooleanField(default=False)

    class Meta:
        db_table = 'quiz\".\"lesson'
        ordering = ['order']

    def __str__(self):
        return f"{self.name_ru}"
