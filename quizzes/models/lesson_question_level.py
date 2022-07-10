from base.abstract_models import *
from django.db import models
from quizzes.models import lesson
from quizzes.models.question_level import QuestionLevel


class LessonQuestionLevel(Ordering):
    lesson = models.ForeignKey(
        lesson.Lesson,
        on_delete=models.CASCADE
    )
    question_level = models.ForeignKey(
        QuestionLevel,
        on_delete=models.CASCADE
    )
    number_of_questions = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.lesson} - {self.question_level}'