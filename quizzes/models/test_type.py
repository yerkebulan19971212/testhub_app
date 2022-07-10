from base.abstract_models import *


class TestType(IsActive, TimeStampedModel, AbstractBaseName, Ordering):
    pass
