from django.contrib import admin

from .models import (Lesson, LessonGroup, LessonPair, TestType, TestTypeLesson,
                     TestTypeLessonGroup)

admin.site.register([
    Lesson,
    LessonGroup,
    LessonPair,
    TestType,
    TestTypeLesson,
    TestTypeLessonGroup
])
