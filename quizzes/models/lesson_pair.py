from django.db import models

from base import abstract_models


class LessonPair(abstract_models.TimeStampedModel):
    # lesson = models.ForeignKey(
    #     'quizzes.Lesson',
    #     related_name='lesson_pairs',
    #     on_delete=models.CASCADE)
    lesson = models.ForeignKey(
        'quizzes.TestTypeLesson',
        related_name='lesson_pairs',
        on_delete=models.CASCADE)
    lesson_group = models.ForeignKey(
        'quizzes.LessonGroup',
        related_name='lesson_pairs',
        on_delete=models.CASCADE)

    class Meta:
        db_table = 'quiz\".\"lesson_pair'

    def __str__(self):
        return self.lessons
