from base.abstract_models import *
from django.db import models
from quizzes.models import lesson
import accounts.models as account


class TestType(IsActive, TimeStampedModel, AbstractBaseName):
    pass


class TestTypeLesson(TimeStampedModel):
    lesson = models.ForeignKey(
        lesson.Lesson,
        on_delete=models.CASCADE,
        blank=True
    )
    test_type = models.ForeignKey(
        TestType,
        on_delete=models.CASCADE,
        blank=True
    )
    main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.test_type} - {self.lesson}"


class CommonQuestion(models.Model):
    text = models.TextField()


class QuestionLevel(AbstractBaseName):
    point = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.name_kz}'


class LessonQuestionLevel(Ordering):
    lesson = models.ForeignKey(
        lesson.Lesson,
        on_delete=models.CASCADE
    )
    question_level = models.ForeignKey(
        QuestionLevel,
        on_delete=models.CASCADE
    )
    number_of_questions = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.lesson} - {self.question_level}'


class Question(Ordering):
    common_question = models.ForeignKey(
        CommonQuestion,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    lesson_question_level = models.ForeignKey(
        LessonQuestionLevel,
        on_delete=models.CASCADE()

    )

    def __str__(self):
        return f'{self.common_question}'


class QuestionAnser(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.question}'


class TagQuestions(models.Model):
    tag = models.ForeignKey(
        lesson.Tag,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.question} - {self.tag}'


class Variant(models.Model):
    variant = models.IntegerField()

    def __str__(self):
        return f'Вариант - {self.variant}'


class VariantQuestion(models.Model):
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.question} - {self.variant}'


class UserVariant(models.Model):
    user = models.ForeignKey(
        account.User,
        on_delete=models.CASCADE
    )
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.user} - {self.variant}'
