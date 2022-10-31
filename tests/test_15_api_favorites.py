from http import HTTPStatus

import pytest

FAVORITE_URL = '/api/recipes/{}/favorite/'
CHECK_URL = '/api/recipes/{}/'


@pytest.mark.django_db
def test_urls_avaialability(api_client, recipe):
    response = api_client.get(FAVORITE_URL.format(recipe.id))
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {FAVORITE_URL} not found'
    )


@pytest.mark.django_db
def test_add_to_favorite_unauthenticated(api_client, recipe):
    response = api_client.post(FAVORITE_URL.format(recipe.id))
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        f'Only authenticated users can send POST requests to {FAVORITE_URL}'
    )


@pytest.mark.django_db
def test_delete_from_favorite_unauthenticated(api_client, recipe):
    response = api_client.delete(FAVORITE_URL.format(recipe.id))
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        f'Only authenticated users can send DELETE requests to {FAVORITE_URL}'
    )


@pytest.mark.django_db
def test_add_to_favorite_not_existing_recipe(api_user_client):
    response = api_user_client.post(FAVORITE_URL.format(1))
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        f'Incorrect response status code {response.status_code} '
        'when trying to add to favorites not existing recipe'
    )


@pytest.mark.django_db
def test_delete_from_favorite_not_existing(api_user_client):
    response = api_user_client.delete(FAVORITE_URL.format(1))
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        f'Incorrect response status code {response.status_code} '
        'when trying to delete from favorites not existing recipe'
    )


@pytest.mark.django_db
def test_add_to_favorite_existing_recipe(api_user_client, five_recipes):
    recipe_id = five_recipes[0].id
    fields = ['id', 'name', 'image', 'cooking_time']
    response = api_user_client.post(FAVORITE_URL.format(recipe_id))
    assert response.status_code == HTTPStatus.CREATED, (
        f'Incorrect response status code {response.status_code} '
        'when trying to add to favorites not existing recipe'
    )
    # Check database response
    response = api_user_client.get(CHECK_URL.format(recipe_id))
    assert response.data['is_favorited'], (
        'Recipe was not added to favorited on database level'
    )
    # Check response fields
    for field in fields:
        assert field in response.data, (
            f'Field {field} is missing or incorrect in response data'
        )


@pytest.mark.django_db
def test_delete_from_favorite_existing_recipe(api_user_client,
                                              api_user_one_favorite_recipe):
    recipe_id = api_user_one_favorite_recipe.id
    response = api_user_client.delete(FAVORITE_URL.format(recipe_id))
    assert response.status_code == HTTPStatus.NO_CONTENT, (
        f'Incorrect response status code {response.status_code} '
        'for successful delete from favorites'
    )
    # Check database response
    response = api_user_client.get(CHECK_URL.format(recipe_id))
    assert not response.data['is_favorited'], (
        'Recipe was not removed from favorited on database level'
    )
