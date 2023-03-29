from django.db import models

from base.abstract_models import TimeStampedModel


class QuestionAnswerImage(TimeStampedModel):
    upload = models.ImageField(upload_to='image/')

    class Meta:
        db_table = 'quiz\".\"question_answer_image'

    def __str__(self):
        return f'{self.upload}'
