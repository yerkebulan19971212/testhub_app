from django.db import models

from base.abstract_models import *
from quizzes.models import lesson
from quizzes.models.test_type import TestType


class TestTypeLesson(TimeStampedModel):
    lesson = models.ForeignKey(
        lesson.Lesson,
        on_delete=models.CASCADE,
        blank=True
    )
    test_type = models.ForeignKey(
        TestType,
        on_delete=models.CASCADE,
        blank=True
    )
    main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.test_type} - {self.lesson}"
