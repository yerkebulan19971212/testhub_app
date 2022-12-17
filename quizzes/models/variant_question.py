from django.db import models

from base import abstract_models


class VariantQuestion(abstract_models.IsActive,
                      abstract_models.Ordering,
                      abstract_models.TimeStampedModel):
    variant = models.ForeignKey('quizzes.Variant', on_delete=models.CASCADE, db_index=True)
    question = models.ForeignKey('quizzes.Question', on_delete=models.CASCADE, db_index=True)

    class Meta:
        db_table = 'quiz\".\"variant_question'

    def __str__(self):
        return f'{self.question} - {self.variant}'
