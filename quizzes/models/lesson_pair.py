from django.db import models

from base import abstract_models


class LessonPair(abstract_models.TimeStampedModel):
    lesson = models.ForeignKey(
        'quizzes.TestTypeLesson',
        related_name='lesson_pairs',
        on_delete=models.CASCADE,
        db_index=True
    )
    lesson_group = models.ForeignKey(
        'quizzes.LessonGroup',
        related_name='lesson_pairs',
        on_delete=models.CASCADE,
        db_index=True
    )

    class Meta:
        db_table = 'quiz\".\"lesson_pair'
