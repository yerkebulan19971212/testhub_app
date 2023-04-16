from django.db import models

from base import abstract_models


class SpecialityDetailInfo(abstract_models.Ordering,
                           abstract_models.TimeStampedModel):
    detail = models.ForeignKey(
        'universities.DetailSpeciality',
        on_delete=models.CASCADE,
        related_name='speciality_detail_infos',
        db_index=True
    )
    value_kz = models.CharField(max_length=128)
    value_ru = models.CharField(max_length=128, default='')
    value_en = models.CharField(max_length=128, default='', null=True,
                                blank=True)
    speciality = models.ForeignKey(
        'quizzes.Speciality',
        on_delete=models.CASCADE,
        related_name='speciality_detail_infos',
        db_index=True
    )

    class Meta:
        db_table = 'universities\".\"speciality_detail_infos'

    def __str__(self):
        return str(self.speciality.name_kz)
