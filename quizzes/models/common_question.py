from django.db import models

from base import abstract_models


class CommonQuestion(abstract_models.TimeStampedModel):
    text = models.TextField(blank=True, null=True, db_index=True)
    file = models.FileField(blank=True, null=True, db_index=True)

    class Meta:
        db_table = 'quiz\".\"common_question'

    # def __str__(self):
    #     return self.pk
