from django.db import models

import accounts.models as account
from quizzes.models.variant import Variant


class UserVariant(models.Model):
    user = models.ForeignKey(
        account.User,
        on_delete=models.CASCADE
    )
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'quiz\".\"user_variant'

    def __str__(self):
        return f'{self.user} - {self.variant}'
