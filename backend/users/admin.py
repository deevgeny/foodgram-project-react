from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Subscriptions, User


@admin.register(User)
class CustomAdminUser(UserAdmin):
    list_filter = ("email", "username")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "email",
                ),
            },
        ),
    )


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    ...
