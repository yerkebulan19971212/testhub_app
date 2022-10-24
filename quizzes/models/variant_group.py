from base import abstract_models


class VariantGroup(abstract_models.AbstractBaseName,
                   abstract_models.IsActive,
                   abstract_models.Ordering,
                   abstract_models.TimeStampedModel):
    class Meta:
        db_table = 'quiz\".\"variant_group'

    def __str__(self):
        return f'{self.name_kz}'
