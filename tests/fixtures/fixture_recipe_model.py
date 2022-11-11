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
def five_recipes(db, five_users, five_tags):
    users = five_users
    tags = five_tags
    recipes = []
    for i in range(len(users)):
        recipes.append(
            Recipe.objects.create(
                author=users[i],
                name=f'Test recipe {i}',
                text=f'Test text {i}',
                cooking_time=10
            )
        )
    for i in range(len(recipes)):
        recipes[i].tags.add(tags[i])
    return recipes


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
