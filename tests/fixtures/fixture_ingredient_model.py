import pytest
from recipes.models import Ingredient


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
