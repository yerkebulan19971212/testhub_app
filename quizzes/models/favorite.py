from django.db import models

from base import abstract_models


class Favorite(abstract_models.TimeStampedModel):
    question = models.ForeignKey(
        'quizzes.Question',
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    is_favorite = models.BooleanField(default=True)

    class Meta:
        db_table = 'quiz\".\"favorite'
        unique_together = ['question', 'user']
        ordering = ['-modified']

    def __str__(self):
        return f"{str(self.question_id)} - {self.user}"
