from django.db import models

from quizzes.models.question import Question
from quizzes.models.tag import Tag


class TagQuestions(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.question} - {self.tag}'
