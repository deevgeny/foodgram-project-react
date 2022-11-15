from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingCart,
    Subscription,
    Tag,
    Unit,
)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'subscriber')
    empty_value_display = '---'


@admin.register(Favorite)
class FavoriteCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = '---'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = '---'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    empty_value_display = '---'


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    empty_value_display = '---'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '---'


@admin.register(IngredientAmount)
class IngredientsListAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')
    empty_value_display = '---'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'favorited', 'recipe_tags',
                    'recipe_ingredients')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)

    @staticmethod
    def favorited(obj):
        """Count number of times recipe is favorited."""
        return obj.favorited_by.count()

    @staticmethod
    def recipe_tags(obj):
        return "\n".join([i[0] for i in obj.tags.values_list('name')])

    @staticmethod
    def recipe_ingredients(obj):
        return "\n".join([i[0] for i in obj.ingredients.values_list('name')])

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Override change view function to add extra arguments."""
        extra_context = extra_context or {}
        # Add recipe favorited count
        extra_context['favorited_title'] = _('Favorited')
        extra_context['favorited_count'] = self.favorited(
            Recipe.objects.get(id=object_id)
        )
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
