import pytest
from recipes.models import IngredientAmount


@pytest.fixture
def ingredient_amount(db, ingredient, recipe):
    return IngredientAmount.objects.create(
        recipe=recipe, ingredient=ingredient, amount=100)


@pytest.fixture
def five_ingredient_amounts(db, recipe, five_ingredients):
    ingredients = five_ingredients
    ingredient_amounts = []
    for amount, ingredient in enumerate(ingredients, start=1):
        ingredient_amounts.append(
            IngredientAmount.objects.create(
                recipe=recipe, ingredient=ingredient, amount=amount
            )
        )
    return ingredient_amounts
