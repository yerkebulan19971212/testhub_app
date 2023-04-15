from django.contrib import admin
from django.db import models
from django.forms import Textarea

from universities.models import LessonGroupSpeciality, UniversityDetail, \
    UniversityImage
from .models import (Answer, CommonQuestion, Favorite, FlashCard, Lesson,
                     LessonGroup, LessonPair, LessonQuestionLevel,
                     NumberOfQuestions, PassAnswer, Question, QuestionLevel,
                     QuizEvent, QuizEventQuestion, TestType, TestTypeLesson,
                     TestTypeLessonGroup, UserVariant, Variant,
                     VariantQuestion, Grade, InfoError, Topic, TopicQuestion,
                     UniversitySpeciality,
                     Country, University, Speciality, ComfortUniversity,
                     Comfort)
from .models.variant_group import VariantGroup

admin.site.register([
    Lesson,
    LessonPair,
    LessonQuestionLevel,
    QuestionLevel,
    TestType,
    TestTypeLesson,
    TestTypeLessonGroup,
    VariantQuestion,
    UserVariant,
    FlashCard,
    NumberOfQuestions,
    CommonQuestion,
    Favorite,
    PassAnswer,
    QuizEvent,
    QuizEventQuestion,
    Grade,
    Topic,
    TopicQuestion,
    UniversitySpeciality,
    Comfort,
    ComfortUniversity,
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


class LessonPairInline(admin.TabularInline):
    model = LessonPair


@admin.register(LessonGroup)
class LessonGroupAdmin(admin.ModelAdmin):
    inlines = [
        LessonPairInline,
    ]


@admin.register(InfoError)
class InfoErrorAdmin(admin.ModelAdmin):
    list_display = (
        'error_name',
        'id',
        'error_type',
        'grade_type',
        'is_active',
        'created',
        'modified'
    )
    search_fields = ('error_name',)
    list_filter = ('is_active', 'error_type', 'grade_type')
    readonly_fields = ('pk', 'created', 'modified')


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = (
        'variant',
        'variant_group',
        'id',
        'sum_question',
        'main',
        'is_active',
        'order',
        'created',
        'modified'
    )
    search_fields = ('variant', 'variant_group__name_kz')
    list_filter = ('variant_group', 'is_active', 'main')
    readonly_fields = ('pk', 'created', 'modified')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'name_kz',
        'name_ru',
        'name_en',
        'id',
        'icon',
        'name_code',
        'is_active',
        'order',
        'created',
        'modified'
    )
    search_fields = (
        'name_kz',
        'name_ru',
        'name_en',
        'id',
        'name_code',
    )
    list_filter = ('is_active',)
    readonly_fields = ('pk', 'created', 'modified')


class SpecialityInline(admin.TabularInline):
    model = UniversitySpeciality
    readonly_fields = ('pk',)
    extra = 0
    can_delete = True
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 80})},
    }


class ComfortUniversityInline(admin.TabularInline):
    model = ComfortUniversity
    readonly_fields = ('pk',)
    extra = 0
    can_delete = True
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 80})},
    }


class UniversityDetailInline(admin.TabularInline):
    model = UniversityDetail
    readonly_fields = ('pk',)
    extra = 0
    can_delete = True
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 80})},
    }

class UniversityImageInline(admin.TabularInline):
    model = UniversityImage
    readonly_fields = ('pk',)
    extra = 0
    can_delete = True
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 80})},
    }


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    inlines = [
        SpecialityInline,
        ComfortUniversityInline,
        UniversityDetailInline,
        UniversityImageInline
    ]
    list_display = (
        'name_kz',
        'name_ru',
        'name_en',
        'id',
        'icon',
        'short_name_kz',
        'short_name_ru',
        'short_name_en',
        'city',
        'name_code',
        'is_active',
        'order',
        'created',
        'modified'
    )
    search_fields = (
        'name_kz',
        'name_ru',
        'name_en',
        'id',
        'name_code',
        'description',
        'address'
    )
    list_filter = ('is_active', 'city', 'city__country')
    readonly_fields = ('pk', 'created', 'modified')


class LessonGroupSpecialityInline(admin.TabularInline):
    model = LessonGroupSpeciality
    readonly_fields = ('pk',)
    extra = 0
    can_delete = True
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 80})},
    }


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    inlines = [
        LessonGroupSpecialityInline
    ]
    list_display = (
        'name_kz',
        'name_ru',
        'name_en',
        'id',
        'icon',
        'short_name_kz',
        'short_name_ru',
        'short_name_en',
        'code',
        'status',
        'description_kz',
        'description_ru',
        'description_en',
        'name_code',
        'is_active',
        'order',
        'created',
        'modified'
    )
    search_fields = (
        'name_kz',
        'name_ru',
        'name_en',
        'id',
        'name_code',
        'description',
        'address'
    )
    list_filter = ('is_active',)
    readonly_fields = ('pk', 'created', 'modified')
