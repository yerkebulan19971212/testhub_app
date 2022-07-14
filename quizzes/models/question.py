from django.db import models

from base import abstract_models


class Question(abstract_models.Ordering,
               abstract_models.IsActive,
               abstract_models.TimeStampedModel):
    common_question = models.ForeignKey(
        'quizzes.CommonQuestion',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    lesson_question_level = models.ForeignKey(
        'quizzes.LessonQuestionLevel',
        on_delete=models.CASCADE)
    question = models.TextField()

    class Meta:
        db_table = 'quiz\".\"question'

    def __str__(self):
        return f'{self.common_question}'
