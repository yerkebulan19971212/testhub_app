from django.db import models

from base import abstract_models


class DetailSpeciality(abstract_models.TimeStampedModel,
                       abstract_models.AbstractBaseNameCode,
                       abstract_models.IsActive,
                       abstract_models.AbstractBaseName):
    icon = models.FileField(upload_to='university_detail')
    is_filter = models.BooleanField(default=False)

    class Meta:
        db_table = 'universities\".\"detail_speciality'

    def __str__(self):
        if self.name_kz:
            return str(self.name_kz)
        return "None"
