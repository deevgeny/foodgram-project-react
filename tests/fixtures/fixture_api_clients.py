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
    client = APIClient()
    data = {
        'email': 'user@fake.com',
        'username': 'user',
        'first_name': 'Vasya',
        'last_name': 'Pupkin',
        'password': 'VeryStrongPassword'
    }
    client.post('/api/users/', data=data)
    return data['password'], data['email']


@pytest.fixture
def api_another_user(db):
    data = {
        'email': 'anotheruser@fake.com',
        'username': 'anotheruser',
        'first_name': 'AnotherVasya',
        'last_name': 'AnotherPupkin',
        'password': 'VeryStrongPassword'
    }
    User.objects.create_user(
        email=data['email'],
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        password=data['password']
    )
    return data['password'], data['email']


@pytest.fixture
def api_user_client(db, api_user):
    client = APIClient()
    password, email = api_user
    response = client.post('/api/auth/token/login/',
                           data={'password': password, 'email': email})
    token = response.json()['auth_token']
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return client


@pytest.fixture
def api_another_user_client(db, api_another_user):
    client = APIClient()
    password, email = api_another_user
    response = client.post('/api/auth/token/login/',
                           data={'password': password, 'email': email})
    token = response.json()['auth_token']
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return client


@pytest.fixture
def create_five_users(db):
    base = ['one', 'two', 'three', 'four', 'five']
    for idx, val in enumerate(base):
        User.objects.create_user(
            email=f'{val}@fake.com',
            username=val,
            first_name=val,
            last_name=val,
            password=f'superpass{val}'
        )
