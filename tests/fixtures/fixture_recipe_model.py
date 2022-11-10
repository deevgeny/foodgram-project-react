import pytest
from recipes.models import Recipe


@pytest.fixture
def recipe(db, user, tag):
    obj = Recipe.objects.create(
        author=user,
        name='Test recipe',
        text='Test text',
        cooking_time=10
    )
    obj.tags.add(tag)
    return obj


@pytest.fixture
def create_recipe(db, user, tag, create_five_ingredient_amounts):
    obj = Recipe.objects.create(
        author=user,
        name='recipe',
        text='Text',
        cooking_time=10
    )
    obj.ingredients.add(*create_five_ingredient_amounts)
    obj.tags.add(tag)
    return obj
