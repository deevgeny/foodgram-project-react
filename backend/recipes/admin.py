from django.contrib import admin

from .models import Subscriptions, Tag


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    ...


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ...
