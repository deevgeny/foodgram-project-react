from http import HTTPStatus

import pytest

SHOPPING_CART_URL = '/api/recipes/download_shopping_cart/'
SHOPPING_CART_ACT_URL = '/api/recipes/{}/shopping_cart/'
SHOPPING_CART_CHECK_URL = '/api/recipes/{}/'


@pytest.mark.django_db
def test_urls_avaialability(api_client, recipe):
    response = api_client.get(SHOPPING_CART_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {SHOPPING_CART_URL} not found'
    )
    response = api_client.get(SHOPPING_CART_ACT_URL.format(recipe.id))
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {SHOPPING_CART_URL} not found'
    )


@pytest.mark.django_db
def test_add_to_shopping_cart_unauthenticated(api_client):
    response = api_client.post(SHOPPING_CART_ACT_URL.format(1))
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Only authenticated users can add recipes to shopping cart'
    )


@pytest.mark.django_db
def test_add_to_shopping_cart_twice(
    api_user_client, api_user_one_recipe_in_shopping_cart
):
    recipe = api_user_one_recipe_in_shopping_cart
    error_key = 'errors'
    error_message = 'recipe already in shopping cart'
    response = api_user_client.post(SHOPPING_CART_ACT_URL.format(recipe.id))
    # Check response status
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        'It is not allowed to add recipe to shopping cart twice'
    )
    # Check response data
    if error_key in response.data:
        assert response.data['errors'][0] == error_message, (
            'Incorrect error message raised by serializer'
        )
    else:
        assert False, (
            'Incorrect or missing response error key for error message'
        )


@pytest.mark.django_db
def test_add_to_shopping_cart_successful(api_user_client, five_recipes):
    recipe = five_recipes[0]
    fields = ['id', 'name', 'image', 'cooking_time']
    response = api_user_client.post(
        SHOPPING_CART_ACT_URL.format(recipe.id)
    )
    # Test status code
    assert response.status_code == HTTPStatus.CREATED, (
        f'Incorrect response status code {response.status_code} for '
        'successfuly added recipe to shopping cart'
    )
    response = api_user_client.get(SHOPPING_CART_CHECK_URL.format(recipe.id))
    # Test response data fields
    for field in fields:
        assert field in response.data, (
            f'Field {field} is missing in response data after '
            'adding recipe to shopping cart successfully'
        )
    # Test database
    assert response.data['is_in_shopping_cart'], (
        'Incorrectly saved data to database'
    )


@pytest.mark.django_db
def test_delete_from_shopping_cart_unauthenticated(api_client):
    response = api_client.delete(SHOPPING_CART_ACT_URL.format(1))
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Only authenticated users allowed to delete recipes '
        'from shopping cart'
    )


@pytest.mark.django_db
def test_delete_from_shopping_cart_not_added_recipe(
    api_user_client, five_recipes
):
    recipe = five_recipes[0]
    response = api_user_client.delete(SHOPPING_CART_ACT_URL.format(recipe.id))
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        f'Incorrect response status code {response.status_code} to the '
        'user attempt to delete recipe from shopping cart which have not '
        'been added to it'
    )


@pytest.mark.django_db
def test_delete_from_shopping_successful(
    api_user_client, api_user_one_recipe_in_shopping_cart
):
    recipe_id = api_user_one_recipe_in_shopping_cart.recipe.id
    response = api_user_client.delete(SHOPPING_CART_ACT_URL.format(recipe_id))
    assert response.status_code == HTTPStatus.NO_CONTENT, (
        f'Incorrect status code {response.status_code} for successfully '
        'deleted recipe from shopping cart'
    )


@pytest.mark.django_db
def test_download_shopping_cart_unuthenticated(api_client):
    response = api_client.get(SHOPPING_CART_URL)
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Only authenticated users can download shopping cart'
    )


@pytest.mark.django_db
def test_download_shopping_cart_successful(
    api_user_client, api_user_one_recipe_in_shopping_cart
):
    response = api_user_client.get(SHOPPING_CART_URL)
    assert response.status_code == HTTPStatus.OK, (
        f'Incorrect response status code {response.status_code} for '
        'successfully downloaded shopping cart pdf file'
    )
