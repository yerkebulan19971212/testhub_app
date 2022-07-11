from django.db import models

from base.abstract_models import *
from quizzes.models import lesson


class LessonPair(models.Model):
    lessons = models.ManyToManyField(lesson.Lesson)

    def __str__(self):
        return self.lessons
