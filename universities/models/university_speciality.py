from django.db import models

from base import abstract_models


class UniversitySpeciality(abstract_models.TimeStampedModel):
    speciality = models.ForeignKey(
        'universities.Speciality',
        on_delete=models.CASCADE,
        related_name='university_specialities',
        db_index=True
    )
    university = models.ForeignKey(
        'universities.University',
        on_delete=models.CASCADE,
        related_name='university_specialities',
        db_index=True
    )
    score = models.IntegerField(default=140)
    grant = models.IntegerField(default=140)
    min_bal = models.IntegerField(default=0)
    min_bal_with_quota = models.IntegerField(default=0)
    avg_cost = models.IntegerField(default=0)

    class Meta:
        db_table = 'universities\".\"university_speciality'

    def __str__(self):
        return str(self.university.name_kz)
