from http import HTTPStatus

import pytest

RECIPES_URL = '/api/recipes/'


@pytest.mark.django_db
def test_urls_availability(api_client, create_recipe):
    response = api_client.get(RECIPES_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {RECIPES_URL} not found'
    )
    response = api_client.get(RECIPES_URL + '1/')
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {RECIPES_URL + "1/"} not found'
    )


@pytest.mark.django_db
def test_urls_unauthenticated_permissions(api_client, create_recipe):
    response = api_client.get(RECIPES_URL)
    assert response.status_code == HTTPStatus.OK, (
        f'GET request to {RECIPES_URL} should be available for all users'
    )
    response = api_client.get(RECIPES_URL + '1/')
    assert response.status_code == HTTPStatus.OK, (
        f'GET request to {RECIPES_URL + "1/"} should be available for all '
        'users'
    )


@pytest.mark.django_db
def test_api_response_fields(api_client, create_recipe):
    fields = [
        'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
        'cooking_time'
    ]
    response = api_client.get(RECIPES_URL + '1/')
    assert len(response.json()) == len(fields), (
        f'Recipe model api response should have {len(fields)} fields'

    )
    for field in fields:
        assert field in response.json(), (
            f'Field name `{field}` is missing or incorrect in Recipe model '
            'api response'
        )


@pytest.mark.django_db
def test_api_response_tag_field_content(api_client, create_recipe):
    fields = ['id', 'name', 'color', 'slug']
    response = api_client.get(RECIPES_URL + '1/')
    assert len(response.json()['tags'][0]) == len(fields), (
        f'Recipe model api response should have {len(fields)} fields inside '
        'tags field.'
    )
    for field in fields:
        assert field in response.json()['tags'][0], (
            f'Field name `{field}` is missing or incorrect inside tags field '
            'of Recipe model api response'
        )


@pytest.mark.django_db
def test_api_response_author_field_content(api_client, create_recipe):
    fields = ['email', 'id', 'username', 'first_name', 'last_name']
    response = api_client.get(RECIPES_URL + '1/')
    assert len(response.json()['author']) == len(fields), (
        f'Recipe model api response should have {len(fields)} fields inside '
        'author field.'
    )
    for field in fields:
        assert field in response.json()['author'], (
            f'Field name `{field}` is missing or incorrect inside author '
            'field of Recipe model api response'
        )


@pytest.mark.django_db
def test_api_response_ingredients_field_content(api_client, create_recipe):
    fields = ['id', 'name', 'measurement_unit', 'amount']
    response = api_client.get(RECIPES_URL + '1/')
    assert len(response.json()['ingredients'][0]) == len(fields), (
        f'Recipe model api response should have {len(fields)} fields inside '
        'ingredients field.'
    )
    for field in fields:
        assert field in response.json()['ingredients'][0], (
            f'Field name `{field}` is missing or incorrect inside ingredients '
            'field of Recipe model api response'
        )
