from django.db import models

from base import abstract_models


class Tag(abstract_models.AbstractBaseName,
          abstract_models.IsActive,
          abstract_models.Ordering,
          abstract_models.TimeStampedModel):
    test_type_lesson = models.ForeignKey(
        'quizzes.TestTypeLesson',
        on_delete=models.CASCADE,
        db_index=True
    )

    class Meta:
        db_table = 'quiz\".\"tag'

    def __str__(self):
        return f"{self.name_ru}"
