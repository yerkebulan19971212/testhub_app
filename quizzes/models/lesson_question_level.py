from django.db import models

from base import abstract_models


class LessonQuestionLevel(abstract_models.Ordering,
                          abstract_models.TimeStampedModel):
    test_type_lesson = models.ForeignKey(
        'quizzes.TestTypeLesson',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='lesson_question_level'
    )
    question_level = models.ForeignKey(
        'quizzes.QuestionLevel',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='lesson_question_level'
    )
    number_of_questions = models.IntegerField(default=0, db_index=True)

    class Meta:
        db_table = 'quiz\".\"lesson_question_level'
        unique_together = ['test_type_lesson', 'question_level']

    def __str__(self):
        return f'{self.test_type_lesson.lesson.name_kz} - {self.question_level}'
