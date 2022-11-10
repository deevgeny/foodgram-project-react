import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def api_user(db, api_client):
    data = {
        'email': 'user@fake.com',
        'username': 'user',
        'first_name': 'Vasya',
        'last_name': 'Pupkin',
        'password': 'VeryStrongPassword'
    }
    api_client.post('/api/users/', data=data)
    return data['password'], data['email']


@pytest.fixture
def api_user_client(db, api_client, api_user):
    password, email = api_user
    response = api_client.post('/api/auth/token/login/',
                               data={'password': password, 'email': email})
    token = response.json()['auth_token']
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return api_client


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
