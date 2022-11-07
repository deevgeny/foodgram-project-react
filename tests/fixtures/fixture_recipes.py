import pytest
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientsList,
    Recipe,
    ShoppingCart,
    Subscription,
    Tag,
    Unit,
)


@pytest.fixture
def subscription(db, user, admin):
    return Subscription.objects.create(
        author=user,
        subscriber=admin
    )


@pytest.fixture
def tag(db):
    return Tag.objects.create(
        name='tasty snack',
        hex_code='#000000',
        slug='tasty_snack'
    )


@pytest.fixture
def create_five_units(db):
    names = ['kg', 'gr', 'pcs', 'ltr', 'cup']
    units = []
    for name in names:
        units.append(Unit.objects.create(name=name))
    return units


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
def ingredients_list(db, ingredient):
    return IngredientsList.objects.create(
        item=ingredient,
        amount=100,
    )


@pytest.fixture
def recipe(db, user, tag, ingredients_list):
    r = Recipe.objects.create(
        author=user,
        name='recipe',
        text='Text',
        cooking_time=10
    )
    r.ingredients.add(ingredients_list)
    r.tag.add(tag)
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
