from django.db import models

from base.abstract_models import *
from quizzes.models import lesson
from quizzes.models.test_type import TestType


class TestTypeLesson(TimeStampedModel):
    lesson = models.ForeignKey(
        lesson.Lesson,
        related_name='test_type_lessons',
        on_delete=models.CASCADE,
        blank=True
    )
    test_type = models.ForeignKey(
        TestType,
        related_name='test_type_lessons',
        on_delete=models.CASCADE,
        blank=True
    )
    main = models.BooleanField(default=False)

    class Meta:
        unique_together = ('test_type', 'lesson')

    def __str__(self):
        return f"{self.id}"
