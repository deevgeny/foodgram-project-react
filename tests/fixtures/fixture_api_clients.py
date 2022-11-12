import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def api_user(db):
    password = 'VeryStrongPassword'
    user = User.objects.create_user(
        email='vasek@fake.com',
        username='vasek',
        first_name='Vasya',
        last_name='Pupkin',
        password=password
    )
    return user, password


@pytest.fixture
def api_another_user(db):
    password = 'VeryStrongPassword'
    user = User.objects.create_user(
        email='kolyanchikus@fake.com',
        username='kolyanchikus',
        first_name='Kolya',
        last_name='Kozyavkin',
        password=password
    )
    return user, password


@pytest.fixture
def api_user_client(db, api_user):
    client = APIClient()
    user, password = api_user
    response = client.post('/api/auth/token/login/',
                           data={'password': password, 'email': user.email})
    token = response.json()['auth_token']
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return client


@pytest.fixture
def api_another_user_client(db, api_another_user):
    client = APIClient()
    another_user, password = api_another_user
    response = client.post('/api/auth/token/login/',
                           data={'password': password,
                                 'email': another_user.email})
    token = response.json()['auth_token']
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return client


@pytest.fixture
def api_five_users(db):
    base = ['one', 'two', 'three', 'four', 'five']
    users = []
    for idx, val in enumerate(base):
        users.append(
            User.objects.create_user(
                email=f'{val}@fake.com',
                username=val,
                first_name=val,
                last_name=val,
                password=f'superpass{idx}'
            )
        )
    return users
