from django.db import models

from base import abstract_models


class Question(abstract_models.Ordering,
               abstract_models.IsActive,
               abstract_models.TimeStampedModel):
    common_question = models.ForeignKey(
        'quizzes.CommonQuestion',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_index=True
    )
    lesson_question_level = models.ForeignKey(
        'quizzes.LessonQuestionLevel',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='questions'
    )
    question = models.TextField(null=True)
    math = models.BooleanField(default=False)
    variant_group = models.ForeignKey(
        'quizzes.VariantGroup',
        on_delete=models.CASCADE,
        db_index=True
    )

    class Meta:
        db_table = 'quiz\".\"question'

    def __str__(self):
        return f'{self.question}'
