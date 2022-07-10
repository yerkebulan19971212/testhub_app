from base.abstract_models import *
from django.db import models
from quizzes.models import lesson


class Tag(AbstractBaseName):
    lesson = models.ForeignKey(
        lesson.Lesson,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name_kz
