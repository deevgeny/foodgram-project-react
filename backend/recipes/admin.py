from django.contrib import admin

from .models import (
    Subscription, Tag, Unit, Ingredient, IngredientsList, Recipe, ShoppingCart,
    Favorite
)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    ...


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ...


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    ...


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    ...


@admin.register(IngredientsList)
class IngredientsListAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    ...


@admin.register(Favorite)
class FavoriteCartAdmin(admin.ModelAdmin):
    ...
