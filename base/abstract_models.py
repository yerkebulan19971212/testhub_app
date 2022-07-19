from django.db import models

from base.abstract_managers import IsActiveManager


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Ordering(models.Model):
    order = models.IntegerField(default=0, db_index=True)

    class Meta:
        abstract = True


class IsActive(models.Model):
    is_active = models.BooleanField(default=True, db_index=True)
    active_manager = IsActiveManager()

    class Meta:
        abstract = True


class AbstractBaseName(models.Model):
    name_kz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)

    class Meta:
        abstract = True


class AbstractBaseTitle(models.Model):
    title_kz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)

    class Meta:
        abstract = True
