from django.db import models

from base import abstract_models


class GrantCount(abstract_models.TimeStampedModel):
    year = models.ForeignKey(
        'universities.Year',
        on_delete=models.CASCADE,
        related_name='grant_counts',
        null=True
    )
    speciality = models.ForeignKey(
        'quizzes.Speciality',
        on_delete=models.CASCADE,
        related_name='grant_counts',
        null=True
    )
    count = models.IntegerField(default=0)

    class Meta:
        db_table = 'universities\".\"grant_count'

    def __str__(self):
        return f"{self.year.name_code} - {self.count}"
