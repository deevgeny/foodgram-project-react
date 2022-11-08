from http import HTTPStatus

import pytest

INGREDIENT_URL = '/api/ingredients/'


@pytest.mark.django_db
def test_urls_availability(api_client, create_five_ingredients):
    response = api_client.get(INGREDIENT_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {INGREDIENT_URL} not found'
    )
    response = api_client.get(INGREDIENT_URL + '1/')
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {INGREDIENT_URL + "1/"} not found'
    )


@pytest.mark.django_db
def test_urls_unauthenticated_permissions(api_client, create_five_ingredients):
    response = api_client.get(INGREDIENT_URL)
    assert response.status_code == HTTPStatus.OK, (
        f'GET request to {INGREDIENT_URL} should be available for all users'
    )
    response = api_client.get(INGREDIENT_URL + '1/')
    assert response.status_code == HTTPStatus.OK, (
        f'GET request to {INGREDIENT_URL +"1/"} should be available for all '
        'users'
    )


@pytest.mark.django_db
def test_ingredients_have_no_pagination(api_client, create_five_ingredients):
    response = api_client.get(INGREDIENT_URL)
    assert 'count' not in response.data, (
        f'URL {INGREDIENT_URL} should not have pagination'
    )


@pytest.mark.django_db
def test_api_response_fields(api_client, create_five_ingredients):
    fields = ['id', 'name', 'measurement_unit']
    response = api_client.get(INGREDIENT_URL + '1/')
    assert len(response.data) == len(fields), (
        f'Ingredient model api response should have {len(fields)} fields'
    )
    for field in fields:
        assert field in response.data, (
            f'Field name `{field}` is missing or incorrect in Ingredient '
            'model api response'
        )


@pytest.mark.django_db
def test_ingredient_not_found(api_client):
    response = api_client.get(INGREDIENT_URL + '1/')
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        f'Incorrect response status code {response.status_code} '
        'for not existing tag'
    )
