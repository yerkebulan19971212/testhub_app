from django.db import models

from base import abstract_models


class QuestionScore(abstract_models.TimeStampedModel):
    user_variant = models.ForeignKey(
        'quizzes.UserVariant',
        on_delete=models.CASCADE,
        related_name='question_score'
    )
    question = models.ForeignKey(
        'quizzes.Question',
        on_delete=models.CASCADE,
        related_name='question_score'
    )
    score = models.IntegerField(default=0)

    class Meta:
        db_table = 'quiz\".\"score'