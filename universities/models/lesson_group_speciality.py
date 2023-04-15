

from django.db import models

from base import abstract_models


class LessonGroupSpeciality(abstract_models.TimeStampedModel):
    lesson_group = models.ForeignKey(
        'quizzes.LessonGroup',
        on_delete=models.CASCADE,
        related_name='lesson_groups_specialities',
        null=True
    )
    speciality = models.ForeignKey(
        'quizzes.Speciality',
        on_delete=models.CASCADE,
        related_name='lesson_groups_specialities',
        db_index=True
    )

    class Meta:
        db_table = 'quiz\".\"lesson_group_speciality'

    def __str__(self):
        object_name = [lp.lesson.lesson.name_kz for lp in
                       self.lesson_group.lesson_pairs.all()]

        return " - ".join(object_name)
