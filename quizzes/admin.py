from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import (Answer, CommonQuestion, Favorite, FlashCard, Lesson,
                     LessonGroup, LessonPair, LessonQuestionLevel,
                     NumberOfQuestions, PassAnswer, Question, QuestionLevel,
                     QuizEvent, QuizEventQuestion, TestType, TestTypeLesson,
                     TestTypeLessonGroup, UserVariant, Variant,
                     VariantQuestion)
from .models.variant_group import VariantGroup

admin.site.register([
    Lesson,
    LessonGroup,
    LessonPair,
    LessonQuestionLevel,

    QuestionLevel,
    TestType,
    TestTypeLesson,
    TestTypeLessonGroup,
    Variant,
    VariantQuestion,
    UserVariant,
    FlashCard,
    NumberOfQuestions,
    CommonQuestion,
    Favorite,
    PassAnswer,
    QuizEvent,
    QuizEventQuestion
])


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'answer', 'correct', 'id', 'question', 'created', 'modified')
    search_fields = ('answer', 'question__question')
    # list_filter = ('question__topic__lesson', 'question__topic',)
    readonly_fields = ('pk', 'created', 'modified')


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ('pk', 'correct', 'answer')
    readonly_fields = ('pk',)
    extra = 0
    # max_num = 4
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 80})},
    }


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = (
        'question', 'id', 'is_active', 'math', 'created', 'modified')

    # list_filter = ['topic__lesson__test_type', 'topic__lesson', 'topic']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 5, 'cols': 180})},
    }


@admin.register(VariantGroup)
class VariantGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name_kz', 'id', 'is_active', 'order', 'created', 'modified')

    # list_filter = ['topic__lesson__test_type', 'topic__lesson', 'topic']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 5, 'cols': 180})},
    }
