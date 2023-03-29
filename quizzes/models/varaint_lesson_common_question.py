from django.db import models

from base import abstract_models


class VariantLessonCommonQuestion(abstract_models.TimeStampedModel):
    variant = models.ForeignKey(
        'quizzes.Variant',
        on_delete=models.CASCADE,
        null=True,
        db_index=True,
        related_name='variant_lesson_common_questions'
    )
    lesson = models.ForeignKey(
        'quizzes.TestTypeLesson',
        on_delete=models.CASCADE,
        null=True,
        db_index=True,
        related_name='variant_lesson_common_questions'
    )
    common_question = models.ForeignKey(
        'quizzes.CommonQuestion',
        on_delete=models.CASCADE,
        null=True,
        db_index=True,
        related_name='variant_lesson_common_questions'
    )

    class Meta:
        db_table = 'quiz\".\"variant_lesson_common_question'

    def __str__(self):
        return f'Вариант - {self.variant}'
