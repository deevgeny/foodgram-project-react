from http import HTTPStatus

import pytest

USERS_URL = '/api/users/'
CURRENT_USER_URL = '/api/users/me/'
LOGIN_URL = '/api/auth/token/login/'
LOGOUT_URL = '/api/auth/token/logout/'
CHANGE_PASSWORD_URL = '/api/users/set_password/'


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
    response = api_client.post(USERS_URL, data=data)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'url {USERS_URL} not found'
    )
    assert response.json() == response_data, (
        'Incorrect response data'
    )
    assert response.status_code == HTTPStatus.CREATED, (
        f'Incorrect response status code {response.status_code}'
    )


@pytest.mark.django_db
def test_user_registration_with_bad_data(api_client):
    data = {
        'username': 'vasek',
        'first_name': 'Vasya',
        'last_name': 'Pupkin',
        'password': 'VasyaStrong'
    }
    response_data = {'email': ['This field is required.']}
    response = api_client.post(USERS_URL, data=data)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'url {USERS_URL} not found'
    )
    assert response.json() == response_data, (
        'Incorrect response data'
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        f'Incorrect response status code {response.status_code}'
    )


@pytest.mark.django_db()
def test_user_login(api_client, api_user):
    password, email = api_user
    response = api_client.post(
        LOGIN_URL, data={'password': password, 'email': email}
    )
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'url {LOGIN_URL} not found'
    )
    assert 'auth_token' in response.json(), (
        'Authorization token is missing in response'
    )
    assert response.status_code == HTTPStatus.CREATED, (
        f'Incorrect response status code {response.status_code}'
    )


@pytest.mark.django_db()
def test_user_login_with_bad_data(api_client):
    response = api_client.post(
        LOGIN_URL, data={'password': 'fakepass', 'email': 'some@fake.com'}
    )
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'url {LOGIN_URL} not found'
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        f'Incorrect response status code {response.status_code}'
    )


@pytest.mark.django_db
def test_user_logout(api_user_client):
    response = api_user_client.post(LOGOUT_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'url {LOGOUT_URL} not found'
    )
    assert response.status_code == HTTPStatus.NO_CONTENT, (
        f'Incorrect response status code {response.status_code}'
    )


@pytest.mark.django_db
def test_user_change_password(api_user, api_user_client):
    password, email = api_user
    data = {'new_password': 'MyNewVeryStrongPassword',
            'current_password': password}
    response = api_user_client.post(CHANGE_PASSWORD_URL, data=data)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'url {CHANGE_PASSWORD_URL} not found'
    )
    assert response.status_code == HTTPStatus.NO_CONTENT, (
        f'Incorrect response status code {response.status_code}'
    )


@pytest.mark.django_db
def test_user_change_password_with_bad_data(api_user, api_user_client):
    password, email = api_user
    data = {'new_password': 'MyNewVeryStrongPassword',
            'current_password': 'BadPassword'}
    response = api_user_client.post(CHANGE_PASSWORD_URL, data=data)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'url {CHANGE_PASSWORD_URL} not found'
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        f'Incorrect response status code {response.status_code}'
    )


@pytest.mark.django_db
def test_user_change_password_not_authorized(api_client):
    data = {'new_password': 'MyNewVeryStrongPassword',
            'current_password': 'BadPassword'}
    response = api_client.post(CHANGE_PASSWORD_URL, data=data)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'url {CHANGE_PASSWORD_URL} not found'
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        f'Incorrect response status code {response.status_code}'
    )


@pytest.mark.django_db
def test_users_list_unauthorized(api_client):
    response = api_client.get(USERS_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {USERS_URL} not found'
    )
    assert response.status_code == HTTPStatus.OK, (
        f'Incorrect response status code {response.status_code}, '
        'users list should be available for all'
    )


@pytest.mark.django_db
def test_users_list_authorized(api_user_client):
    response = api_user_client.get(USERS_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {USERS_URL} not found'
    )
    assert response.status_code == HTTPStatus.OK, (
        f'Incorrect response status code {response.status_code}, '
        'users list should be available for all'
    )


@pytest.mark.django_db
def test_users_list_pagination(api_client):
    # Add fixture with many users creation
    ...


@pytest.mark.django_db
def test_user_info_by_id_unauthorized(api_user, api_client):
    ...


@pytest.mark.django_db
def test_user_info_by_id_authorized(api_user, api_client):
    # Add fixture with many users creation
    ...


@pytest.mark.django_db
def test_current_user_info_unauthorized(api_client):
    response = api_client.get(CURRENT_USER_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {CURRENT_USER_URL} not found'
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        f'Incorrect response status code {response.status_code}, '
        'current user information should be available for '
        'authorized users only'
    )


@pytest.mark.django_db
def test_current_user_info_authorized(api_user, api_user_client):
    password, email = api_user
    response = api_user_client.get(CURRENT_USER_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {CURRENT_USER_URL} not found'
    )
    assert response.status_code == HTTPStatus.OK, (
        f'Incorrect response status code {response.status_code}, '
        'current user information should be available for '
        'authorized users only'
    )
    assert response.json()['email'] == email, (
        f'Incorrect current user information on {CURRENT_USER_URL}'
    )
