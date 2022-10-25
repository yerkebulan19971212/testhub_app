from django.db import models

from base import abstract_models
from base.constant import QuizzesType, Status


class QuizEvent(abstract_models.TimeStampedModel):
    quizzes_type = models.CharField(
        max_length=128,
        choices=QuizzesType.choices(),
        null=True,
        db_index=True
    )
    test_type_lesson = models.ForeignKey(
        'quizzes.TestTypeLesson',
        on_delete=models.CASCADE,
        null=True,
        db_index=True,
        related_name='quiz_event'
    )
    status = models.CharField(
        max_length=128,
        choices=Status.choices(),
        default=Status.NOT_PASSED
    )

    class Meta:
        db_table = 'quiz\".\"quiz_event'


class QuizEventQuestion(abstract_models.TimeStampedModel):
    quiz_event = models.ForeignKey(
        QuizEvent,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='quiz_event_questions'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        related_name='quiz_event_questions'
    )
    question = models.ForeignKey(
        'quizzes.Question',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='quiz_event_questions'
    )

    class Meta:
        db_table = 'quiz\".\"quiz_event_question'
