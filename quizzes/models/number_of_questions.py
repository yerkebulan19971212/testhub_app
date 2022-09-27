from django.db import models

from base.abstract_models import TimeStampedModel


class NumberOfQuestions(TimeStampedModel):
    # question_type = models.CharField(max_length=128)
    numbers = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Нумерация вопросов"
        verbose_name_plural = 'Нумерация вопросов'
        db_table = 'quiz\".\"number_of_questions'

    def __str__(self):
        return f"{self.numbers}"
