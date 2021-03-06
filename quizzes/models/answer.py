from django.db import models

from base import abstract_models


class Answer(abstract_models.TimeStampedModel):
    question = models.ForeignKey(
        'quizzes.Question', related_name='answers', on_delete=models.CASCADE)
    answer = models.TextField()
    correct = models.BooleanField(default=False)

    class Meta:
        db_table = 'quiz\".\"answer'

    def __str__(self):
        return f'{self.question}'
