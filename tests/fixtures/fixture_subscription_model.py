import pytest
from recipes.models import Subscription


@pytest.fixture
def subscription(db, user, admin):
    return Subscription.objects.create(
        author=user,
        subscriber=admin
    )
