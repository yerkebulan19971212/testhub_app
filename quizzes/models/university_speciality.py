from django.db import models

from base import abstract_models


class UniversitySpeciality(abstract_models.TimeStampedModel):
    speciality = models.ForeignKey(
        'quizzes.Speciality',
        on_delete=models.CASCADE,
        related_name='university_specialities',
        db_index=True
    )
    university = models.ForeignKey(
        'quizzes.University',
        on_delete=models.CASCADE,
        related_name='university_specialities',
        db_index=True
    )

    class Meta:
        db_table = 'quiz\".\"university_speciality'

    def __str__(self):
        return str(self.university.name_kz)
