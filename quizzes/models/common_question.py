from django.db import models


class CommonQuestion(models.Model):
    text = models.TextField()
