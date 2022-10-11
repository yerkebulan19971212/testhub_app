from django.contrib import admin

from .models import (Lesson, LessonGroup, LessonPair, LessonQuestionLevel,
                     Question, QuestionLevel, TestType, TestTypeLesson,
                     TestTypeLessonGroup, UserVariant, Variant, Answer,
                     VariantQuestion, NumberOfQuestions, FlashCard,
                     CommonQuestion)

admin.site.register([
    Lesson,
    LessonGroup,
    LessonPair,
    LessonQuestionLevel,
    Question,
    QuestionLevel,
    TestType,
    TestTypeLesson,
    TestTypeLessonGroup,
    Variant,
    VariantQuestion,
    UserVariant,
    FlashCard,
    NumberOfQuestions,
    CommonQuestion
])


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'correct', 'id', 'question', )
