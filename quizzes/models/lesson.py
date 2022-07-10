from base.abstract_models import *
from django.db import models


class Lesson(AbstractBaseName):

    def __str__(self):
        return self.name_kz


class LessonPair(models.Model):
    lessons = models.ManyToManyField(Lesson)

    def __str__(self):
        return self.lessons


class Tag(AbstractBaseName):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name_kz
