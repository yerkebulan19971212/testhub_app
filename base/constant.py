from enum import Enum

from django.utils.translation import ugettext_lazy as _


class Choice(Enum):
    @classmethod
    def choices(cls):
        return [(c.value, _(c.name)) for c in cls]

    @classmethod
    def repr(cls):
        return {c.name: {'id': c.value, 'name': _(c.name)} for c in cls}

    @classmethod
    def list(cls):
        return [c.value for c in cls]

    def __str__(self):
        return self.value


class Role(str, Choice):
    SUPER_ADMIN = 'SUPER_ADMIN'
    TEACHER = 'TEACHER'
    CURATOR = 'CURATOR'
    STUDENT = 'STUDENT'


class TestLang(int, Choice):
    KAZAKH = 0
    RUSSIAN = 1
