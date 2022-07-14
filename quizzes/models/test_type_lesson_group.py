from django.db import models

from base import abstract_models


class TestTypeLessonGroup(abstract_models.TimeStampedModel):
    test_type = models.ForeignKey(
        'quizzes.TestType',
        related_name='test_type_lesson_groups',
        on_delete=models.CASCADE)
    lesson_group = models.ForeignKey(
        'quizzes.LessonGroup',
        related_name='test_type_lesson_groups',
        on_delete=models.CASCADE)

    class Meta:
        db_table = 'quiz\".\"test_type_lesson_group'

    def __str__(self):
        return self.pk
