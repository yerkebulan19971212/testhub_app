from django.db import models

from base.abstract_models import (AbstractBaseName, IsActive, Ordering,
                                  TimeStampedModel)


class TestType(AbstractBaseName,
               IsActive,
               Ordering,
               TimeStampedModel):
    icon = models.ImageField(upload_to='test_type')

    def __str__(self):
        return f"{self.name_ru}"
