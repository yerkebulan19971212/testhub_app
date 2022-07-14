from django.db import models

from base import abstract_models


class QuestionLevel(abstract_models.AbstractBaseName,
                    abstract_models.IsActive,
                    abstract_models.TimeStampedModel):
    point = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'quiz\".\"question_level'

    def __str__(self):
        return f'{self.name_kz}'
