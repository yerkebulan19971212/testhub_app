from django.db import models

from base.abstract_models import AbstractBaseName, IsActive, TimeStampedModel
from quizzes.models import lesson


class Tag(AbstractBaseName,
          IsActive,
          TimeStampedModel):
    lesson = models.ForeignKey(
        lesson.Lesson,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name_kz
