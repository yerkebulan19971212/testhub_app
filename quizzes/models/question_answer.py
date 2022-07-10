from base.abstract_models import *
from django.db import models
from quizzes.models import lesson
from quizzes.models.question import Question


class QuestionAnswer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.question}'
