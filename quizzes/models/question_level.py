from django.db import models

from base import abstract_models
from base.constant import ChoiceType


class QuestionLevel(abstract_models.AbstractBaseName,
                    abstract_models.AbstractBaseNameCode,
                    abstract_models.IsActive,
                    abstract_models.Ordering,
                    abstract_models.TimeStampedModel):
    point = models.PositiveSmallIntegerField(default=0)
    choice = models.PositiveSmallIntegerField(
        choices=ChoiceType.choices(),
        default=ChoiceType.CHOICE)

    class Meta:
        db_table = 'quiz\".\"question_level'

    def __str__(self):
        return f'{self.name_kz}'
