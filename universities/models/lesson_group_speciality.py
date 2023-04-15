

from django.db import models

from base import abstract_models


class LessonGroupSpeciality(abstract_models.TimeStampedModel):
    lesson_group = models.ForeignKey(
        'quizzes.LessonGroup',
        on_delete=models.CASCADE,
        related_name='lesson_groups_specialities',
        null=True
    )
    value = models.CharField(max_length=128)
    dimension = models.CharField(max_length=128, default='', null=True, blank=True)
    university = models.ForeignKey(
        'quizzes.Speciality',
        on_delete=models.CASCADE,
        related_name='lesson_groups_specialities',
        db_index=True
    )

    class Meta:
        db_table = 'quiz\".\"lesson_group_speciality'

    def __str__(self):
        return str(self.university.name_kz)
