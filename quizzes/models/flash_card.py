from base.abstract_models import TimeStampedModel
from django.db import models


class FlashCard(TimeStampedModel):
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='flash_cards'
    )
    question = models.ForeignKey(
        'quizzes.Question',
        on_delete=models.CASCADE,
        related_name='flash_cards'
    )
    passed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Флэш карта"
        verbose_name_plural = 'Флэш карты'
        db_table = 'quiz\".\"flash_card'

    def __str__(self):
        return f"{self.user},  {self.question},  {self.passed}"
