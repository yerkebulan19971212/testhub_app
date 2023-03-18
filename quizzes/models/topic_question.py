from django.db import models

from base import abstract_models


class TopicQuestion(abstract_models.AbstractBaseName,
                    abstract_models.IsActive,
                    abstract_models.Ordering,
                    abstract_models.TimeStampedModel):
    topic = models.ForeignKey(
        'quizzes.Topic',
        on_delete=models.CASCADE, related_name='topic_questions',
        db_index=True
    )
    question = models.ForeignKey(
        'quizzes.Question',
        on_delete=models.CASCADE,
        related_name='topic_questions',
        db_index=True
    )

    class Meta:
        db_table = 'quiz\".\"topic_question'

    def __str__(self):
        return f'{self.topic.name_ru} - {self.question.pk}'
