from base.abstract_models import (AbstractBaseName, IsActive, Ordering,
                                  TimeStampedModel)


class Lesson(AbstractBaseName,
             Ordering,
             TimeStampedModel, IsActive):

    def __str__(self):
        return self.name_kz


