import pytest
from django.contrib.auth import get_user_model
from recipes.models import ShoppingCart

User = get_user_model()


@pytest.fixture
def shopping_cart(db, user, recipe):
    return ShoppingCart.objects.create(
        user=user,
        recipe=recipe
    )


@pytest.fixture
def api_user_one_recipe_in_shopping_cart(db, api_user, five_recipes):
    _, email = api_user
    user = User.objects.get(email=email)
    return ShoppingCart.objects.create(user=user, recipe=five_recipes[0])
