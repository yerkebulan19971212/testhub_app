from django.db import models

from base import abstract_models


class LessonQuestionLevel(abstract_models.Ordering,
                          abstract_models.TimeStampedModel):
    test_type_lesson = models.ForeignKey(
        'quizzes.TestTypeLesson',
        on_delete=models.CASCADE)
    question_level = models.ForeignKey(
        'quizzes.QuestionLevel',
        on_delete=models.CASCADE)
    number_of_questions = models.IntegerField(default=0)

    class Meta:
        db_table = 'quiz\".\"lesson_question_level'
        unique_together = ['test_type_lesson', 'question_level']

    # def __str__(self):
    #     return f'{self.lesson} - {self.question_level}'
