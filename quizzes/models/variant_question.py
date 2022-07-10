from django.db import models

from quizzes.models.question import Question
from quizzes.models.variant import Variant


class VariantQuestion(models.Model):
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.question} - {self.variant}'
