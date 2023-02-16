from django.db import models

from base import abstract_models


class QuestionQuizEventScore(abstract_models.TimeStampedModel):
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        related_name='quiz_event_score'
    )
    quiz_event = models.ForeignKey(
        'quizzes.QuizEvent',
        on_delete=models.CASCADE,
        related_name='quiz_event_score'
    )
    question = models.ForeignKey(
        'quizzes.Question',
        on_delete=models.CASCADE,
        related_name='quiz_event_scores'
    )
    score = models.IntegerField(default=0)

    class Meta:
        db_table = 'quiz\".\"quiz_event_score'
