from django.db import models

from base import abstract_models


class Topic(abstract_models.AbstractBaseName,
            abstract_models.IsActive,
            abstract_models.Ordering,
            abstract_models.AbstractBaseNameCode,
            abstract_models.TimeStampedModel):
    test_type_lesson = models.ForeignKey(
        'quizzes.TestTypeLesson',
        on_delete=models.CASCADE,
        db_index=True,
        null=True
    )

    class Meta:
        db_table = 'quiz\".\"topic'

    def __str__(self):
        return f"{self.name_ru}"
