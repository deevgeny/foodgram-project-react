import pytest
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()


@pytest.fixture
def recipe(db, api_user, tag):
    _, email = api_user
    user = User.objects.get(email=email)
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
    obj.tags.add(tag)
    return obj
