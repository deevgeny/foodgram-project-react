import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create(
        username='TestUser', email='testuser@fg.fake', first_name='Vasya',
        last_name='Pupkin'
    )


@pytest.fixture
def admin(db):
    return User.objects.create(
        username='AdminUser', email='adminuser@fake.com', first_name='Kolya',
        last_name='Nosov', is_staff=True
    )


@pytest.fixture
def superuser(db):
    return User.objects.create(
        username='SuperUser', email='superuser@fake.com', first_name='Misha',
        last_name='Kozyavkin', is_staff=True, is_superuser=True
    )
