from django.db import models

from base import abstract_models


class GrantUniversityCount(abstract_models.TimeStampedModel):
    year = models.ForeignKey(
        'universities.Year',
        on_delete=models.CASCADE,
        related_name='grant_university_counts',
        null=True
    )
    university_speciality = models.ForeignKey(
        'quizzes.UniversitySpeciality',
        on_delete=models.CASCADE,
        related_name='grant_university_counts',
        null=True
    )
    count = models.IntegerField(default=0)

    class Meta:
        db_table = 'universities\".\"grant_university_count'

    def __str__(self):
        return f"{self.year.name_code} - {self.count}"
