from django.db import models

from base.abstract_models import AbstractBaseName


class QuestionLevel(AbstractBaseName):
    point = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.name_kz}'
