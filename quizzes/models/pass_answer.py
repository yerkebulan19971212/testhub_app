from django.db import models

from base import abstract_models
from base.constant import QuizzesType


class PassAnswer(abstract_models.TimeStampedModel):
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='pass_answers'
    )
    question = models.ForeignKey(
        'quizzes.Question',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='pass_answers'
    )
    answer = models.ForeignKey(
        'quizzes.Answer',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='pass_answers'
    )
    quizzes_type = models.CharField(
        max_length=128,
        choices=QuizzesType.choices(),
        null=True,
        db_index=True
    )

    class Meta:
        db_table = 'quiz\".\"pass_answer'
