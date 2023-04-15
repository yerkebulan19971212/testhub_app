from django.contrib import admin
from django.db import models
from django.forms import Textarea

from quizzes.admin import SpecialityInline, ComfortUniversityInline
from quizzes.models import University
from universities.models import (UniversityImage, Detail, UniversityDetail,
                                 LessonGroupSpeciality)

admin.site.register([
    UniversityImage,
    UniversityDetail,
    Detail,
    LessonGroupSpeciality
])

class UniversityImageInline(admin.TabularInline):
    model = UniversityImage
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


# @admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    inlines = [
        SpecialityInline,
        ComfortUniversityInline,
        UniversityImageInline,
        # UniversityDetailImageInline
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
        'address_kz',
        'address_ru',
        'address_en',
        'description_kz',
        'description_ru',
        'description_en',
        'city',
        # 'country',
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
#
#
#
# @admin.register(Speciality)
# class SpecialityAdmin(admin.ModelAdmin):
#     list_display = (
#         'name_kz',
#         'name_ru',
#         'name_en',
#         'id',
#         'icon',
#         'short_name_kz',
#         'short_name_ru',
#         'short_name_en',
#         'code',
#         'status',
#         'description_kz',
#         'description_ru',
#         'description_en',
#         'name_code',
#         'is_active',
#         'order',
#         'created',
#         'modified'
#     )
#     search_fields = (
#         'name_kz',
#         'name_ru',
#         'name_en',
#         'id',
#         'name_code',
#         'description',
#         'address'
#     )
#     list_filter = ('is_active',)
#     readonly_fields = ('pk', 'created', 'modified')
