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
            f'Field name {field} is missing or incorrect in Ingredient '
            'model api response'
        )


@pytest.mark.django_db
def test_ingredient_not_found(api_client):
    response = api_client.get(INGREDIENT_URL + '1/')
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        f'Incorrect response status code {response.status_code} '
        'for not existing tag'
    )


@pytest.mark.django_db
def test_ingredient_search_with_full_keyword(api_client,
                                             create_five_ingredients):
    search_param = 'search'
    data = {search_param: 'potato'}
    custom_search_param = 'name'
    custom_data = {custom_search_param: 'potato'}
    response = api_client.get(INGREDIENT_URL, data=data)
    assert len(response.data) != 1, (
        f'Standard search_param={search_param} should be overriden'
    )
    response = api_client.get(INGREDIENT_URL, data=custom_data)
    assert len(response.data) == 1, (
        'Search with full keyword does not work with '
        f' search_param={custom_search_param} and full search keyword'
    )


@pytest.mark.django_db
def test_ingredient_search_with_partial_keyword(api_client,
                                                create_five_ingredients):
    data = {'name': 'po'}
    response = api_client.get(INGREDIENT_URL, data=data)
    assert len(response.data) == 1, (
        'Search keyword is not a substring of search field value'
    )
