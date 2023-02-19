from django.db import models

from base.abstract_models import TimeStampedModel
from base.constant import GradeType


class Grade(TimeStampedModel):
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='grade'
    )
    grade_ball = models.IntegerField(
        choices=GradeType.choices(),
    )
    grade_error = models.ForeignKey(
        'quizzes.InfoError',
        on_delete=models.CASCADE,
        related_name='grade',
        null=True
    )
    user_variant = models.ForeignKey(
        'quizzes.UserVariant',
        on_delete=models.CASCADE,
        related_name='grade',
        null=True
    )
    comment = models.TextField(null=True)

    class Meta:
        db_table = 'info\".\"grade'
