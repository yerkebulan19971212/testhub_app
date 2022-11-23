from django.db import models

import accounts.models as account
from base.constant import Status
from quizzes.models.variant import Variant


class UserVariant(models.Model):
    user = models.ForeignKey(
        account.User,
        on_delete=models.CASCADE,
        related_name='user_variant'
    )
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        related_name='user_variant'
    )
    status = models.CharField(
        max_length=128,
        choices=Status.choices(),
        default=Status.NOT_PASSED
    )

    class Meta:
        db_table = 'quiz\".\"user_variant'

    def __str__(self):
        return f'{self.user} - {self.variant}'
