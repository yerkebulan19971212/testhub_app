from django.db import models

from base import abstract_models


class Mark(abstract_models.TimeStampedModel):
    question = models.ForeignKey(
        'quizzes.Question',
        on_delete=models.CASCADE,
        related_name='marks'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='marks'
    )
    user_variant = models.ForeignKey(
        'quizzes.UserVariant',
        on_delete=models.CASCADE,
        related_name='marks'
    )
    is_mark = models.BooleanField(default=True)

    class Meta:
        db_table = 'quiz\".\"mark'
        unique_together = ['question', 'user', 'user_variant']
        ordering = ['-modified']

    def __str__(self):
        return f"{str(self.question_id)} - {self.user}"
