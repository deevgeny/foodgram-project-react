from http import HTTPStatus
from pathlib import Path

import pytest
from django.conf import settings

from recipes.models import Recipe

RECIPES_URL = '/api/recipes/'


@pytest.mark.django_db
def test_urls_availability(api_client, recipe):
    response = api_client.get(RECIPES_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {RECIPES_URL} not found'
    )
    response = api_client.get(RECIPES_URL + '1/')
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {RECIPES_URL + "1/"} not found'
    )


@pytest.mark.django_db
def test_urls_unauthenticated_permissions(api_client, recipe):
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
def test_api_response_fields(api_client, recipe):
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
def test_api_response_tag_field_content(api_client, recipe):
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
def test_api_response_author_field_content(api_client, recipe):
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
def test_api_response_ingredients_field_content(api_client,
                                                five_ingredient_amounts):
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
def test_create_recipe_by_authorized_user(api_user_client, ingredient, tag):
    data = {
        'ingredients': [{'id': ingredient.id, 'amount': 10}],
        'tags': [tag.id],
        'image': ('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA'
                  'AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxA'
                  'GVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=='),
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
    # Check field names in response
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
    # Clean up image files
    obj = Recipe.objects.get(id=response.data['id'])
    path = Path().joinpath(settings.MEDIA_ROOT).joinpath(obj.image.name)
    path.unlink()


@pytest.mark.django_db
def test_create_recipe_by_unauthenticated_user(api_client, ingredient, tag):
    data = {
        'ingredients': [{'id': ingredient.id, 'amount': 10}],
        'tags': [tag.id],
        'image': ('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA'
                  'AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxA'
                  'GVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=='),
        'name': 'Test recipe',
        'text': 'Test recipe description',
        'cooking_time': 5
    }
    response = api_client.post(RECIPES_URL, data=data, format='json')
    # Check response status
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Only authorized users can create recipes'
    )


@pytest.mark.django_db
def test_patch_recipe_by_author(api_user_client, recipe, five_tags,
                                five_ingredients):
    data = {
        'ingredients': [
            {'id': i.id, 'amount': 10} for i in five_ingredients
        ],
        'tags': [i.id for i in five_tags],
        'image': ('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA'
                  'AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxA'
                  'GVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=='),
        'name': 'New name',
        'text': 'New text',
        'cooking_time': 100
    }
    # Check that recipe does not have image
    assert recipe.image.name == '', (
        'Recipe.image field should be empty before running patch test'
    )
    response = api_user_client.patch(RECIPES_URL + f'{recipe.id}/', data=data,
                                     format='json')
    assert response.status_code == HTTPStatus.OK, (
        f'Incorrect response status code {response.status_code} for '
        f'successful PATCH request to {RECIPES_URL}'
    )
    # Check recipe in database
    check_fields = ['name', 'text', 'cooking_time']
    response = api_user_client.get(RECIPES_URL + f'{recipe.id}/')
    assert response.status_code == HTTPStatus.OK, (
        'Could not get recipe from database via api request to check fields'
    )
    for field in check_fields:
        assert response.data[field] == data[field], (
            f'Recipe.{field} field was not updated'
        )
    assert response.data['image'] is not None, (
        'Recipe.image field was not updated'
    )
    assert len(response.data['ingredients']) == len(data['ingredients']), (
        'Recipe.ingredients field was not updated'
    )
    assert len(response.data['tags']) == len(data['tags']), (
        'Recipe.tags field was not updated'
    )
    # Clean up image files
    obj = Recipe.objects.get(id=response.data['id'])
    path = Path().joinpath(settings.MEDIA_ROOT).joinpath(obj.image.name)
    path.unlink()


@pytest.mark.django_db
def test_patch_recipe_by_another_author(api_another_user_client, recipe,
                                        five_tags, five_ingredients):
    data = {
        'ingredients': [
            {'id': i.id, 'amount': 10} for i in five_ingredients
        ],
        'tags': [i.id for i in five_tags],
        'image': ('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA'
                  'AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxA'
                  'GVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=='),
        'name': 'New name',
        'text': 'New text',
        'cooking_time': 100
    }
    # Check that recipe does not have image
    assert recipe.image.name == '', (
        'Recipe.image field should be empty before running patch test'
    )
    response = api_another_user_client.patch(RECIPES_URL + f'{recipe.id}/',
                                             data=data, format='json')
    assert response.status_code == HTTPStatus.FORBIDDEN, (
        'Recipe can be update only by author'
    )
    # Check recipe in database
    check_fields = ['name', 'text', 'cooking_time']
    response = api_another_user_client.get(RECIPES_URL + f'{recipe.id}/')
    assert response.status_code == HTTPStatus.OK, (
        'Could not get recipe from database via api request to check fields'
    )
    for field in check_fields:
        assert response.data[field] != data[field], (
            f'Recipe.{field} field was updated by another user'
        )
    assert response.data['image'] is None, (
        'Recipe.image field was updated by another user'
    )
    assert len(response.data['ingredients']) != len(data['ingredients']), (
        'Recipe.ingredients field was updated by another user'
    )
    assert len(response.data['tags']) != len(data['tags']), (
        'Recipe.tags field was updated by another user'
    )


@pytest.mark.django_db
def test_patch_recipe_by_unauthenticated_user(api_client, recipe, five_tags,
                                              five_ingredients):
    data = {
        'ingredients': [
            {'id': i.id, 'amount': 10} for i in five_ingredients
        ],
        'tags': [i.id for i in five_tags],
        'image': ('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA'
                  'AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxA'
                  'GVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=='),
        'name': 'New name',
        'text': 'New text',
        'cooking_time': 100
    }
    # Check that recipe does not have image
    assert recipe.image.name == '', (
        'Recipe.image field should be empty before running patch test'
    )
    response = api_client.patch(RECIPES_URL + f'{recipe.id}/', data=data,
                                format='json')
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Recipe can be update only by author'
    )
    # Check recipe in database
    check_fields = ['name', 'text', 'cooking_time']
    response = api_client.get(RECIPES_URL + f'{recipe.id}/')
    assert response.status_code == HTTPStatus.OK, (
        'Could not get recipe from database via api request to check fields'
    )
    for field in check_fields:
        assert response.data[field] != data[field], (
            f'Recipe.{field} field was updated by unauthenticated user'
        )
    assert response.data['image'] is None, (
        'Recipe.image field was updated by unauthenticated user'
    )
    assert len(response.data['ingredients']) != len(data['ingredients']), (
        'Recipe.ingredients field was updated by unauthenticated user'
    )
    assert len(response.data['tags']) != len(data['tags']), (
        'Recipe.tags field was updated by unauthenticated user'
    )


@pytest.mark.django_db
def test_delete_recipe_by_author(api_user_client, recipe):
    response = api_user_client.delete(RECIPES_URL + f'{recipe.id}/')
    assert response.status_code == HTTPStatus.NO_CONTENT, (
        f'Incorrect response status code {response.status_code} for '
        f'successful DELETE request to {RECIPES_URL}'
    )
    # Check recipe was deleted from database
    response = api_user_client.get(RECIPES_URL + f'{recipe.id}/')
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Recipe was not deleted from database'
    )


@pytest.mark.django_db
def test_delete_recipe_by_another_user(recipe, api_another_user_client):
    response = api_another_user_client.delete(RECIPES_URL + f'{recipe.id}/')
    assert response.status_code == HTTPStatus.FORBIDDEN, (
        'Recipes can be deleted only by author'
    )


@pytest.mark.django_db
def test_delete_recipe_by_unauthenticated_user(api_client, recipe):
    response = api_client.delete(RECIPES_URL + f'{recipe.id}/')
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Unauthorized user should not have permission to delete recipes'
    )
