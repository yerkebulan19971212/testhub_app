from django.db import models

from base import abstract_models


class UniversityDetail(abstract_models.Ordering,
                       abstract_models.TimeStampedModel):
    detail = models.ForeignKey(
        'universities.Detail',
        on_delete=models.CASCADE,
        related_name='university_details',
        db_index=True
    )
    value = models.CharField(max_length=128)
    dimension = models.CharField(max_length=128, default='', null=True, blank=True)
    university = models.ForeignKey(
        'quizzes.University',
        on_delete=models.CASCADE,
        related_name='university_details',
        db_index=True
    )

    class Meta:
        db_table = 'quiz\".\"university_detail'

    def __str__(self):
        return str(self.university.name_kz)
