import pytest
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingCart,
    Subscription,
    Unit,
)


@pytest.fixture
def subscription(db, user, admin):
    return Subscription.objects.create(
        author=user,
        subscriber=admin
    )


@pytest.fixture
def unit(db):
    return Unit.objects.create(name='kg')


@pytest.fixture
def create_five_units(db):
    names = ['kg', 'gr', 'pcs', 'ltr', 'cup']
    units = []
    for name in names:
        units.append(Unit.objects.create(name=name))
    return units


@pytest.fixture
def ingredient(db, unit):
    return Ingredient.objects.create(name='potato', measurement_unit=unit)


@pytest.fixture
def create_five_ingredients(db, create_five_units):
    units = create_five_units
    names = ['potato', 'sheese', 'apple', 'milk', 'sugar']
    ingredients = []
    for i in zip(names, units):
        ingredients.append(
            Ingredient.objects.create(name=i[0], measurement_unit=i[1]))
    return ingredients


@pytest.fixture
def ingredient_amount(db, ingredient):
    return IngredientAmount.objects.create(ingredient=ingredient, amount=100)


@pytest.fixture
def create_five_ingredients_list(db, create_five_ingredients):
    ingredients = create_five_ingredients
    ingredients_list = []
    for amount, ingredient in enumerate(ingredients, start=1):
        ingredients_list.append(IngredientAmount.objects.create(
            item=ingredient,
            amount=100,
        )
        )
    return ingredients_list


@pytest.fixture
def recipe(db, user, tag, ingredients_list):
    r = Recipe.objects.create(
        author=user,
        name='recipe',
        text='Text',
        cooking_time=10
    )
    r.ingredients.add(ingredients_list)
    r.tags.add(tag)
    return r


@pytest.fixture
def create_recipe(db, user, tag, create_five_ingredients_list):
    r = Recipe.objects.create(
        author=user,
        name='recipe',
        text='Text',
        cooking_time=10
    )
    r.ingredients.add(*create_five_ingredients_list)
    r.tags.add(tag)
    return r


@pytest.fixture
def shopping_cart(db, user, recipe):
    return ShoppingCart.objects.create(
        user=user,
        recipe=recipe
    )


@pytest.fixture
def favorite(db, user, recipe):
    return Favorite.objects.create(
        user=user,
        recipe=recipe
    )
