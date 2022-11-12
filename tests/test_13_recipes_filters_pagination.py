from http import HTTPStatus

import pytest

RECIPES_URL = '/api/recipes/'


@pytest.mark.django_db
def test_recipe_pagination_unauthenticated(api_client, five_recipes):
    data = {'limit': 1}
    response = api_client.get(RECIPES_URL, data=data)
    assert response.status_code == HTTPStatus.OK, (
        f'Incorrect response status code {response.status_code}, '
    )
    assert 'next' in response.data, (
        'PageNumberPaginator should be used'
    )
    if response.data['next']:
        assert 'limit=' in response.data['next'], (
            'PageNumberPaginator should be overiden with '
            'page_size_query_param="limit"'
        )
    else:
        assert len(response.data['results']) == 1, (
            'PageNumberPaginator should return one recipe in results.'
            'Probably PageNumberPaginator should be overiden with '
            'page_size_query_param="limit"'
        )


@pytest.mark.django_db
def test_recipe_filter_by_is_favorited(api_user_client,
                                       api_user_one_favorite_recipe):
    data = {'is_favorited': 1}
    response = api_user_client.get(RECIPES_URL, data=data)
    assert len(response.data['results']) == data['is_favorited'], (
        f'Incorrect work of is_favorited filter with data={data}'
    )


@pytest.mark.django_db
def test_recipe_filter_by_is_favorited_unauthenticated(
    api_client, api_user_one_favorite_recipe
):
    data = {'is_favorited': 1}
    response = api_client.get(RECIPES_URL, data=data)
    assert len(response.data['results']) == 5, (
        f'Incorrect work of is_favorited filter with data={data} '
        'for unauthenticated user'
    )


@pytest.mark.django_db
def test_recipe_filter_by_is_in_shopping_cart(
    api_user_client, api_user_one_recipe_in_shopping_cart
):
    data = {'is_in_shopping_cart': 1}
    response = api_user_client.get(RECIPES_URL, data=data)
    assert len(response.data['results']) == 1, (
        f'Incorrect work of is_in_shopping_cart filter with data={data}'
    )


@pytest.mark.django_db
def test_recipe_filter_by_is_in_shopping_cart_unauthenticated(
    api_client, api_user_one_recipe_in_shopping_cart
):
    data = {'is_in_shopping_cart': 1}
    response = api_client.get(RECIPES_URL, data=data)
    assert len(response.data['results']) == 5, (
        f'Incorrect work of is_in_shopping_cart filter with data={data} '
        'for unauthenticated user'
    )


@pytest.mark.django_db
def test_recipe_filter_by_author(api_user_client, five_recipes):
    data = {'author': five_recipes[0].author.id}
    response = api_user_client.get(RECIPES_URL, data=data)
    assert len(response.data['results']) == 1, (
        f'Incorrect work of author filter with data={data}'
    )


@pytest.mark.django_db
def test_recipe_filter_by_tags(api_user_client, five_recipes):
    recipes = five_recipes
    # Check tags filter with one tag
    one_tag_data = {'tags': recipes[0].tags.all()[0].slug}
    response = api_user_client.get(RECIPES_URL, data=one_tag_data)
    assert len(response.data['results']) == 1, (
        f'Incorrect work of tags filter with data={one_tag_data}'
    )
    # Check tags filter with multiple tags url
    multiple_tags_url = (
        f'{RECIPES_URL}?tags={recipes[0].tags.all()[0].slug}&'
        f'tags={recipes[1].tags.all()[0].slug}'
    )
    response = api_user_client.get(multiple_tags_url)
    assert len(response.data['results']) == 2, (
        f'Incorrect work of tags filter with multiple tags in URL '
        f'{multiple_tags_url}'
    )
