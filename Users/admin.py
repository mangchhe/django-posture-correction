from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from .models import UsersDB

# Register your models here.

admin.site.register(UsersDB)
"""
@admin.register(models.UsersDB)
class CustomUserAdmin(UserAdmin):

    #Custom User Admin

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "user_birth",
                )
            },
        ),
    )

    #list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "email",
    )
"""