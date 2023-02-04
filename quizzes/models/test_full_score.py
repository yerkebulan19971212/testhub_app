from django.db import models

import accounts.models as account
from base import abstract_models


class TestFullScore(abstract_models.TimeStampedModel):
    user = models.ForeignKey(
        account.User,
        on_delete=models.CASCADE,
        related_name='test_full_score',
        db_index=True
    )
    user_variant = models.ForeignKey(
        'quizzes.UserVariant',
        on_delete=models.CASCADE,
        related_name='test_full_score',
        db_index=True
    )
    test_type_lesson = models.ForeignKey(
        'quizzes.TestTypeLesson',
        on_delete=models.CASCADE,
        related_name='test_full_score',
        db_index=True,
        null=True
    )
    unattem = models.IntegerField(default=0)
    user_score = models.IntegerField(default=0)
    number_of_question = models.IntegerField(default=0)
    number_of_score = models.IntegerField(default=0)
    accuracy = models.IntegerField(default=0)

    class Meta:
        db_table = 'quiz\".\"test_full_score'

    # def __str__(self):
    #     return f'{self.name_kz}'
