from django.contrib import admin

from .models import (Lesson, LessonGroup, LessonPair, LessonQuestionLevel,
                     Question, QuestionLevel, TestType, TestTypeLesson,
                     TestTypeLessonGroup, UserVariant, Variant,
                     VariantQuestion)

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
    UserVariant
])
