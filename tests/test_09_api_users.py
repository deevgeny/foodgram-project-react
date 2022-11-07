from http import HTTPStatus

import pytest

USERS_URL = '/api/users/'
CURRENT_USER_URL = '/api/users/me/'
LOGIN_URL = '/api/auth/token/login/'
LOGOUT_URL = '/api/auth/token/logout/'
CHANGE_PASSWORD_URL = '/api/users/set_password/'


@pytest.mark.django_db
def test_url_availability(api_client, api_user, create_five_users):
    response = api_client.get(USERS_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {USERS_URL} not found'
    )
    response = api_client.post(LOGIN_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {LOGIN_URL} not found'
    )
    response = api_client.post(LOGOUT_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {LOGOUT_URL} not found'
    )
    response = api_client.post(CHANGE_PASSWORD_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {CHANGE_PASSWORD_URL} not found'
    )
    response = api_client.get(USERS_URL + '1/')
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {USERS_URL + "1/"} not found'
    )
    response = api_client.get(USERS_URL + '5/')
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {USERS_URL + "5/"} not found'
    )
    response = api_client.get(CURRENT_USER_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {CURRENT_USER_URL} not found'
    )
    response = api_client.post(LOGIN_URL[:-1])
    assert response.status_code != HTTPStatus.MOVED_PERMANENTLY, (
        f'Improper configuration of URL {LOGIN_URL} in urls.py '
        'use re_path() with regex expression to prevent redirection for '
        f'address without trailing slash {LOGIN_URL[:-1]}'
    )
    response = api_client.post(LOGOUT_URL[:-1])
    assert response.status_code != HTTPStatus.MOVED_PERMANENTLY, (
        f'Improper configuration of URL {LOGOUT_URL} in urls.py '
        'use re_path() with regex expression to prevent redirection for '
        f'address without trailing slash {LOGOUT_URL[:-1]}'
    )


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
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        f'Incorrect response status code {response.status_code}'
    )


@pytest.mark.django_db
def test_user_logout(api_user_client):
    response = api_user_client.post(LOGOUT_URL)
    assert response.status_code == HTTPStatus.NO_CONTENT, (
        f'Incorrect response status code {response.status_code}'
    )


@pytest.mark.django_db
def test_user_change_password(api_user, api_user_client):
    password, email = api_user
    data = {'new_password': 'MyNewVeryStrongPassword',
            'current_password': password}
    response = api_user_client.post(CHANGE_PASSWORD_URL, data=data)
    assert response.status_code == HTTPStatus.NO_CONTENT, (
        f'Incorrect response status code {response.status_code}'
    )


@pytest.mark.django_db
def test_user_change_password_with_bad_data(api_user, api_user_client):
    password, email = api_user
    data = {'new_password': 'MyNewVeryStrongPassword',
            'current_password': 'BadPassword'}
    response = api_user_client.post(CHANGE_PASSWORD_URL, data=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        f'Incorrect response status code {response.status_code}'
    )


@pytest.mark.django_db
def test_user_change_password_not_authorized(api_client):
    data = {'new_password': 'MyNewVeryStrongPassword',
            'current_password': 'BadPassword'}
    response = api_client.post(CHANGE_PASSWORD_URL, data=data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        f'Incorrect response status code {response.status_code}'
    )


@pytest.mark.django_db
def test_users_list_unauthorized(api_client):
    response = api_client.get(USERS_URL)
    assert response.status_code == HTTPStatus.OK, (
        f'Incorrect response status code {response.status_code}, '
        'users list should be available for all'
    )


@pytest.mark.django_db
def test_users_list_authorized(api_user_client):
    response = api_user_client.get(USERS_URL)
    assert response.status_code == HTTPStatus.OK, (
        f'Incorrect response status code {response.status_code}, '
        'users list should be available for all'
    )


@pytest.mark.django_db
def test_users_list_pagination_unauthorized(api_client, create_five_users):
    data = {'limit': 1}
    response = api_client.get(USERS_URL, data=data)
    assert response.status_code == HTTPStatus.OK, (
        f'Incorrect response status code {response.status_code}, '
    )
    assert 'next' in response.json(), (
        'PageNumberPaginator should be used'
    )
    if response.json()['next']:
        assert 'limit=' in response.json()['next'], (
            'PageNumberPaginator should be overiden with '
            '`page_size_query_param="limit"`'
        )
    else:
        assert response.json()['next'], (
            'PageNumberPaginator should be overiden with '
            '`page_size_query_param="limit"`'
        )


@pytest.mark.django_db
def test_user_info_by_id_unauthorized(api_client):
    response = api_client.get(USERS_URL + '1/')
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        f'Incorrect response status code {response.status_code}, '
        'unauthorized user is not allowed to access another user information'
    )


@pytest.mark.django_db
def test_user_info_by_id_authorized(api_user_client, create_five_users):
    response = api_user_client.get(USERS_URL + '5/')
    assert response.status_code == HTTPStatus.OK, (
        f'Incorrect response status code {response.status_code}, '
        'authorized user is allowed to access another user information'
    )


@pytest.mark.django_db
def test_not_existing_user_info_by_id_authorized(
    api_user_client, create_five_users
):
    response = api_user_client.get(USERS_URL + '10/')
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Incorrect response status for not existing user'
    )


@pytest.mark.django_db
def test_current_user_info_unauthorized(api_client):
    response = api_client.get(CURRENT_USER_URL)
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        f'Incorrect response status code {response.status_code}, '
        'current user information should be available for '
        'authorized users only'
    )


@pytest.mark.django_db
def test_current_user_info_authorized(api_user, api_user_client):
    password, email = api_user
    response = api_user_client.get(CURRENT_USER_URL)
    assert response.status_code == HTTPStatus.OK, (
        f'Incorrect response status code {response.status_code}, '
        'current user information should be available for '
        'authorized users only'
    )
    assert response.json()['email'] == email, (
        f'Incorrect current user information on {CURRENT_USER_URL}'
    )
