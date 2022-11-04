from http import HTTPStatus

import pytest

reg_url = '/api/users/'
login_url = '/api/auth/token/login/'
logout_url = '/api/auth/token/logout/'
change_password_url = '/api/users/set_password/'


@pytest.mark.django_db
def test_user_registration(api_client):
    data = {
        'email': 'vasya@fake.com',
        'username': 'vasek',
        'first_name': 'Vasya',
        'last_name': 'Pupkin',
        'password': 'VasyaStrong'
    }
    response_data = {
        'email': 'vasya@fake.com',
        'id': 1,
        'username': 'vasek',
        'first_name': 'Vasya',
        'last_name': 'Pupkin',
    }
    response = api_client.post(reg_url, data=data)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'url {reg_url} not found'
    )
    assert response.data == response_data, (
        'Incorrect response data'
    )
    assert response.status_code == HTTPStatus.CREATED, (
        f'Incorrect response status code {response.status_code}'
    )


@pytest.mark.django_db
def test_user_registration_with_bad_data(api_client):
    ...


@pytest.mark.django_db
def test_user_login(api_client):
    data = {
        'email': 'vasya@fake.com',
        'username': 'vasek',
        'first_name': 'Vasya',
        'last_name': 'Pupkin',
        'password': 'VasyaStrong'
    }
    api_client.post(reg_url, data=data)
    response = api_client.post(
        login_url, data={'password': data['password'], 'email': data['email']}
    )
    assert 'auth_token' in response.data
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.django_db
def test_user_logout():
    ...


@pytest.mark.django_db
def test_user_change_password():
    ...
