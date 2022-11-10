import pytest
from recipes.models import Favorite


@pytest.fixture
def favorite(db, user, recipe):
    return Favorite.objects.create(
        user=user,
        recipe=recipe
    )
