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
    response = api_client.post(RECIPES_URL)
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        f'POST request to {RECIPES_URL} should be available only for '
        'authenticated users'
    )


@pytest.mark.django_db
def test_api_response_fields(api_client, create_recipe):
    fields = [
        'id', 'tags', 'author', 'ingredients', 'is_favorited',
        'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
    ]
    response = api_client.get(RECIPES_URL + '1/')
    assert len(response.data) == len(fields), (
        f'Recipe model api response should have {len(fields)} fields'

    )
    for field in fields:
        assert field in response.data, (
            f'Field name `{field}` is missing or incorrect in Recipe model '
            'api response'
        )


@pytest.mark.django_db
def test_api_response_tag_field_content(api_client, create_recipe):
    fields = ['id', 'name', 'color', 'slug']
    response = api_client.get(RECIPES_URL + '1/')
    assert len(response.data['tags'][0]) == len(fields), (
        f'Recipe model api response should have {len(fields)} fields inside '
        'tags field.'
    )
    for field in fields:
        assert field in response.data['tags'][0], (
            f'Field name `{field}` is missing or incorrect inside tags field '
            'of Recipe model api response'
        )


@pytest.mark.django_db
def test_api_response_author_field_content(api_client, create_recipe):
    fields = ['email', 'id', 'username', 'first_name', 'last_name',
              'is_subscribed']
    response = api_client.get(RECIPES_URL + '1/')
    assert len(response.data['author']) == len(fields), (
        f'Recipe model api response should have {len(fields)} fields inside '
        'author field.'
    )
    for field in fields:
        assert field in response.data['author'], (
            f'Field name `{field}` is missing or incorrect inside author '
            'field of Recipe model api response'
        )


@pytest.mark.django_db
def test_api_response_ingredients_field_content(api_client, create_recipe):
    fields = ['id', 'name', 'measurement_unit', 'amount']
    response = api_client.get(RECIPES_URL + '1/')
    assert len(response.data['ingredients'][0]) == len(fields), (
        f'Recipe model api response should have {len(fields)} fields inside '
        'ingredients field.'
    )
    for field in fields:
        assert field in response.data['ingredients'][0], (
            f'Field name `{field}` is missing or incorrect inside ingredients '
            'field of Recipe model api response'
        )


@pytest.mark.django_db
def test_create_recipe(api_user_client, ingredient, tag):
    data = {
        'ingredients': [{'id': ingredient.id, 'amount': 10}],
        'tags': [tag.id],
        'name': 'Test recipe',
        'text': 'Test recipe description',
        'cooking_time': 5
    }
    fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
              'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time']
    tags_fields = ['id', 'name', 'color', 'slug']
    author_fields = ['email', 'id', 'username', 'first_name', 'last_name',
                     'is_subscribed']
    ingredients_fields = ['id', 'name', 'measurement_unit', 'amount']
    response = api_user_client.post(RECIPES_URL, data=data, format='json')
    # Check response status
    assert response.status_code == HTTPStatus.CREATED, (
        f'Incorrect response status code {response.status_code} for '
        f'successful POST request to {RECIPES_URL}'
    )
    # Check number of fields in response
    assert len(response.data) == len(fields), (
        f'POST request to {RECIPES_URL} should return response with '
        f'{len(fields)} fields'
    )
    # Check field namdes in response
    for field in fields:
        assert field in response.data, (
            f'Field name `{field}` is missing or incorrect in response '
            f'after POST request to {RECIPES_URL}'
        )
    # Check number of fields inside response tags field
    assert len(response.data['tags'][0]) == len(tags_fields), (
        f'POST request to {RECIPES_URL} should return response with '
        f'{len(fields)} fields inside tags field'
    )
    # Check field names inside response tags field
    for field in tags_fields:
        assert field in response.data['tags'][0], (
            f'Field name `{field}` is missing or incorrect inside response '
            f'tags field after POST request to {RECIPES_URL}'
        )
    # Check number of fields inside response author field
    assert len(response.data['author']) == len(author_fields), (
        f'POST request to {RECIPES_URL} should return response with '
        f'{len(fields)} fields inside author field'
    )
    # Check field names inside response author fields
    for field in author_fields:
        assert field in response.data['author'], (
            f'Field name `{field}` is missing or incorrect inside response '
            f'author field after POST request to {RECIPES_URL}'
        )
    # Check number of fields inside response ingredients field
    assert len(response.data['ingredients'][0]) == len(ingredients_fields), (
        f'POST request to {RECIPES_URL} should return response with '
        f'{len(fields)} fields inside ingredients field'
    )
    # Check field names inside response ingredients field
    for field in ingredients_fields:
        assert field in response.data['ingredients'][0], (
            f'Field name `{field}` is missing or incorrect inside response '
            f'ingredients field after POST request to {RECIPES_URL}'
        )
