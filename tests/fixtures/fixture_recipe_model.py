import pytest
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()


@pytest.fixture
def recipe(db, api_user, tag):
    user, _ = api_user
    obj = Recipe.objects.create(
        author=user,
        name='Test recipe',
        text='Test text',
        cooking_time=10
    )
    obj.tags.add(tag)
    return obj


@pytest.fixture
def five_recipes(db, api_five_users, five_tags):
    users = api_five_users
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
def another_user_five_recipes(db, api_another_user, five_tags):
    another_user, _ = api_another_user
    tags = five_tags
    recipes = []
    for i in range(5):
        recipes.append(
            Recipe.objects.create(
                author=another_user,
                name=f'Test recipe {i}',
                text=f'Test text {i}',
                cooking_time=10
            )
        )
    for recipe, tag in zip(recipes, tags):
        recipe.tags.add(tag)
    return recipes
