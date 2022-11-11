import pytest
from django.contrib.auth import get_user_model
from recipes.models import Favorite

User = get_user_model()


@pytest.fixture
def favorite(db, user, recipe):
    return Favorite.objects.create(
        user=user,
        recipe=recipe
    )


@pytest.fixture
def api_user_one_favorite_recipe(db, api_user, five_recipes):
    _, email = api_user
    user = User.objects.get(email=email)
    return Favorite.objects.create(user=user, recipe=five_recipes[0])
