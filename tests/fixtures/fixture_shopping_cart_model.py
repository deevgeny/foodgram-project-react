import pytest
from recipes.models import ShoppingCart


@pytest.fixture
def shopping_cart(db, user, recipe):
    return ShoppingCart.objects.create(
        user=user,
        recipe=recipe
    )
