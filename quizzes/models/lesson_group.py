from django.db import models

from base import abstract_models


class LessonGroup(abstract_models.TimeStampedModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    main = models.BooleanField(default=False)

    class Meta:
        db_table = 'quiz\".\"lesson_group'

    def __str__(self):
        object_name = [lp.lesson.lesson.name_kz for lp in self.lesson_pairs.all()]

        return " - ".join(object_name)
