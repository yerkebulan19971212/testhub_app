from base import abstract_models
from django.db import models


class Year(abstract_models.TimeStampedModel,
           abstract_models.AbstractBaseNameCode,
           abstract_models.IsActive):
    date = models.DateField()

    class Meta:
        db_table = 'universities\".\"year'

    def __str__(self):
        if self.name_code:
            return str(self.name_code)
        return "None"
