import pytest
from django.contrib.auth import get_user_model
from recipes.models import Subscription

User = get_user_model()


@pytest.fixture
def subscription(db, api_user, api_another_user):
    user, _ = api_user
    another_user, _ = api_another_user
    return Subscription.objects.create(
        author=another_user,
        subscriber=user
    )


@pytest.fixture
def five_subscriptions(db, api_user, api_five_users):
    user, _ = api_user
    authors = api_five_users
    subs = []
    for author in authors:
        subs.append(
            Subscription.objects.create(
                author=author,
                subscriber=user
            )
        )
    return subs
