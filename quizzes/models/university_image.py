from django.db import models

from base import abstract_models


class UniversityImage(abstract_models.TimeStampedModel):
    image = models.FileField(upload_to='university')
    university = models.ForeignKey(
        'quizzes.University',
        on_delete=models.CASCADE,
        related_name='university_images',
        db_index=True
    )

    class Meta:
        db_table = 'quiz\".\"university_image'

    def __str__(self):
        return str(self.university.name_kz)
