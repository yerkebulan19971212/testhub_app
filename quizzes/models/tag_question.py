from django.db import models

from base import abstract_models


class TagQuestion(abstract_models.AbstractBaseName,
                  abstract_models.IsActive,
                  abstract_models.Ordering,
                  abstract_models.TimeStampedModel):
    tag = models.ForeignKey(
        'quizzes.Tag',
        on_delete=models.CASCADE, related_name='tag_questions',
        db_index=True
    )
    question = models.ForeignKey(
        'quizzes.Question',
        on_delete=models.CASCADE,
        related_name='tag_questions',
        db_index=True
    )

    class Meta:
        db_table = 'quiz\".\"tag_question'

    def __str__(self):
        return f'{self.tag.name_ru} - {self.question.pk}'
