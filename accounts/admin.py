from django.contrib import admin

from .models import Role, User, EmailOTP,PhoneOTP,UserTestType
admin.site.register(EmailOTP)
admin.site.register(PhoneOTP)
admin.site.register(UserTestType)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["id", 'name']
    search_fields = ["name"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "is_superuser",
        "role",
        "created",
        "modified"
    ]
    search_fields = ["email"]
    list_filter = ['role', 'is_superuser']