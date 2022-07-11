from django.db import models

from base.abstract_models import *
from quizzes.models.common_question import CommonQuestion
from quizzes.models.lesson_question_level import LessonQuestionLevel


class Question(Ordering):
    common_question = models.ForeignKey(
        CommonQuestion,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    lesson_question_level = models.ForeignKey(
        LessonQuestionLevel,
        on_delete=models.CASCADE

    )

    def __str__(self):
        return f'{self.common_question}'
