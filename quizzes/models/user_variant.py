from django.db import models

import accounts.models as account
from base.constant import Status
from quizzes.models.variant import Variant


class UserVariant(models.Model):
    user = models.ForeignKey(
        account.User,
        on_delete=models.CASCADE,
        related_name='user_variant',
        db_index=True
    )
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        related_name='user_variant',
        db_index=True
    )
    status = models.CharField(
        max_length=128,
        choices=Status.choices(),
        default=Status.NOT_PASSED,
        db_index=True
    )
    lesson_group = models.ForeignKey(
        'quizzes.LessonGroup',
        on_delete=models.CASCADE,
        related_name='user_variants',
        null=True
    )
    test_start_time = models.DateTimeField(null=True, blank=True)
    test_end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'quiz\".\"user_variant'

    def __str__(self):
        return f'{self.user} - {self.variant}'
