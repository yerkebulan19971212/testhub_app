from django.db import models

from base import abstract_models


class PassAnswer(abstract_models.TimeStampedModel):
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='pass_answers'
    )
    quiz_event = models.ForeignKey(
        'quizzes.QuizEvent',
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
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

    class Meta:
        db_table = 'quiz\".\"pass_answer'
