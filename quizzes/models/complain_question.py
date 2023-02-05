from django.db import models

from base.abstract_models import TimeStampedModel


class ComplainQuestion(TimeStampedModel):
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='complain_questions'
    )
    complain_error = models.ForeignKey(
        'quizzes.InfoError',
        on_delete=models.CASCADE,
        related_name='complain_questions',
        null=True
    )
    question = models.ForeignKey(
        'quizzes.Question',
        on_delete=models.CASCADE,
        related_name='complain_questions',
        null=True
    )
    comment = models.TextField(null=True)

    class Meta:
        db_table = 'info\".\"complain_question'
