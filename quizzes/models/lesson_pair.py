from base.abstract_models import *
from django.db import models
from quizzes.models import lesson

class LessonPair(models.Model):
    lessons = models.ManyToManyField(lesson.Lesson)

    def __str__(self):
        return self.lessons
