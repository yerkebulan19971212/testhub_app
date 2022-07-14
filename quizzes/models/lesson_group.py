from django.db import models

from base import abstract_models


class LessonGroup(abstract_models.TimeStampedModel):
    main = models.BooleanField(default=False)

    class Meta:
        db_table = 'quiz\".\"lesson_group'

    def __str__(self):
        return self.pk
