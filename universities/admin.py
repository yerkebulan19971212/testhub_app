from django.contrib import admin
from django.db import models
from django.forms import Textarea

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
