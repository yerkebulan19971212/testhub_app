from django.db import models

from base.abstract_models import *
from base.constant import TestLang
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
    lang = models.IntegerField(
        choices=TestLang.choices(),
        default=TestLang.KAZAKH)
    main = models.BooleanField(default=False)
    questions_number = models.IntegerField(default=1)

    class Meta:
        unique_together = ('test_type', 'lesson')

    def __str__(self):
        return f"{self.lesson.name_kz}"
