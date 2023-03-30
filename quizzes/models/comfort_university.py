from django.db import models

from base import abstract_models


class ComfortUniversity(abstract_models.TimeStampedModel):
    comfort = models.ForeignKey(
        'quizzes.Comfort',
        on_delete=models.CASCADE,
        related_name='comfort_university',
        db_index=True
    )
    university = models.ForeignKey(
        'quizzes.University',
        on_delete=models.CASCADE,
        related_name='comfort_university',
        db_index=True
    )

    class Meta:
        db_table = 'quiz\".\"comfort_university'

    def __str__(self):
        return str(self.university.name_kz)
