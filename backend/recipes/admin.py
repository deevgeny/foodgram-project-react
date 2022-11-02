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
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(IngredientsList)
class IngredientsListAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorited_count')
    list_filter = ('author', 'name', 'tag')

    def favorited_count(self, obj):
        '''Count number of times recipe is favorited.'''
        return obj.is_favorited.count()
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        '''Override change view function to add extra arguments.'''
        extra_context = extra_context or {}
        # Add recipe favorited count
        count = Favorite.objects.filter(recipe=object_id).count()
        extra_context['favorited'] = count
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    ...


@admin.register(Favorite)
class FavoriteCartAdmin(admin.ModelAdmin):
    ...
