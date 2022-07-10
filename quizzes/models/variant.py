from django.db import models


class Variant(models.Model):
    variant = models.IntegerField()

    def __str__(self):
        return f'Вариант - {self.variant}'
