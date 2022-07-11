from django.db import models

from base.abstract_models import TimeStampedModel
from quizzes.models import lesson
from quizzes.models.question import Question


class QuestionAnswer(TimeStampedModel):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )


    def __str__(self):
        return f'{self.question}'
