from base import abstract_models


class AnswerSign(abstract_models.AbstractBaseNameCode,
                 abstract_models.IsActive,
                 abstract_models.Ordering,
                 abstract_models.TimeStampedModel):
    pass

    class Meta:
        db_table = 'quiz\".\"answer_sign'

    def __str__(self):
        return f'{self.name_code}'
