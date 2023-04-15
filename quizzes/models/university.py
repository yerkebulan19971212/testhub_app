from django.db import models

from base import abstract_models
from quizzes.models import Comfort
from universities.models import UniversityImage, Detail


class University(abstract_models.AbstractBaseName,
              abstract_models.AbstractBaseNameCode,
              abstract_models.IsActive,
              abstract_models.Ordering,
              abstract_models.TimeStampedModel):
    icon = models.FileField(upload_to='university')
    video_link = models.CharField(max_length=255, null=True, blank=True)
    short_name_kz = models.CharField(max_length=255, null=True)
    short_name_ru = models.CharField(max_length=255, null=True)
    short_name_en = models.CharField(max_length=255, null=True)
    phone_number = models.TextField(null=True)
    instagram = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    whatsapp = models.URLField(null=True, blank=True)
    description_kz = models.TextField(null=True)
    description_ru = models.TextField(null=True)
    description_en = models.TextField(null=True)
    city = models.ForeignKey(
        'accounts.City',
        related_name='universities',
        on_delete=models.CASCADE,
        db_index=True
    )
    comforts = models.ManyToManyField(Comfort, through='quizzes.ComfortUniversity')
    # details = models.ManyToManyField(Detail, through='universities.UniversityDetail')

    # country = models.ForeignKey(
    #     'quizzes.Country',
    #     related_name='universities',
    #     on_delete=models.CASCADE,
    #     db_index=True
    # )

    class Meta:
        db_table = 'quiz\".\"university'

    def __str__(self):
        return f' {self.name_ru}'
