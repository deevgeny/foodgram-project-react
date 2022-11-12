from http import HTTPStatus

import pytest

SUBSCRIPTION_LIST_URL = '/api/users/subscriptions/'
SUBSCRIPTION_ACT_URL = '/api/users/{}/subscribe/'


@pytest.mark.django_db
def test_urls_avaialability(api_client):
    response = api_client.get(SUBSCRIPTION_LIST_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {SUBSCRIPTION_LIST_URL} not found'
    )


@pytest.mark.django_db
def test_subscriptions_unauthenticated(api_client):
    response = api_client.get(SUBSCRIPTION_LIST_URL)
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        f'URL {SUBSCRIPTION_LIST_URL} is available for unauthenticated user'
    )


@pytest.mark.django_db
def test_subscriptions_authenticated(api_user_client):
    response = api_user_client.get(SUBSCRIPTION_LIST_URL)
    assert response.status_code == HTTPStatus.OK, (
        f'URL {SUBSCRIPTION_LIST_URL} is not available for authenticated user'
    )


@pytest.mark.django_db
def test_subscriptions_response_fields(api_user_client, subscription):
    response_fields = ['count', 'next', 'previous', 'results']
    subscription_fields = ['email', 'id', 'username', 'first_name',
                           'last_name', 'is_subscribed', 'recipes',
                           'recipes_count']
    response = api_user_client.get(SUBSCRIPTION_LIST_URL)
    # Test response fields
    for field in response_fields:
        assert field in response.data, (
            f'Field {field} is missing of incorrect in response data, '
            'it could be the reason of missing pagnation'
        )
    # Test subscription response fields
    for field in subscription_fields:
        assert field in response.data['results'][0], (
            f'Field {field} is missing or incorrect in response data '
            'results field'
        )


@pytest.mark.django_db
def test_add_subscriptions(api_user_client, api_another_user):
    user, _ = api_another_user
    fields = ['email', 'id', 'username', 'first_name', 'last_name',
              'is_subscribed', 'recipes', 'recipes_count']
    response = api_user_client.post(SUBSCRIPTION_ACT_URL.format(user.id))
    # Test response status code
    assert response.status_code == HTTPStatus.CREATED, (
        f'Incorrect response code {response.status_code} for created '
        'subscription'
    )
    # Test response fields
    for field in fields:
        assert field in response.data, (
            f'Field {field} is missing or incorrect in response data'
        )


@pytest.mark.django_db
def test_add_subscriptions_with_recipes_limit(
    api_user_client, api_another_user, another_user_five_recipes
):
    user = another_user_five_recipes[0].author
    data = {'recipes_limit': 1}
    response = api_user_client.post(
        SUBSCRIPTION_ACT_URL.format(user.id), data=data, format='json')
    assert len(response.data['recipes']) == data['recipes_limit'], (
        'Incorrect work of recipes_limit query parameter'
    )
    assert response.data['recipes_count'] == 5, (
        'Incorrect recipes_count value'
    )


@pytest.mark.django_db
def test_add_subscriptions_unauthenticated(api_client, api_another_user):
    user, _ = api_another_user
    response = api_client.post(SUBSCRIPTION_ACT_URL.format(user.id))
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        'Unauthenticated users are not allowed to add subscriptions'
    )


@pytest.mark.django_db
def test_delete_subscriptions_successful(api_user_client, subscription):
    # Delete subscription
    response = api_user_client.delete(
        SUBSCRIPTION_ACT_URL.format(subscription.author.id)
    )
    assert response.status_code == HTTPStatus.NO_CONTENT, (
        f'Incorrect status code {response.status_code} for deleted '
        'subscription'
    )
    # Check database
    response = api_user_client.get(SUBSCRIPTION_LIST_URL)
    if 'count' in response.data:
        assert response.data['count'] == 0, (
            'Subscription object was not deleted from database'
        )
    else:
        assert len(response.data) == 0, (
            'Subscription object was not deleted from database'
        )


@pytest.mark.django_db
def test_delete_subscriptions_not_found(api_user_client):
    response = api_user_client.delete(SUBSCRIPTION_ACT_URL.format(5))
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        f'Incorrect status code {response.status_code} for not not existing '
        'subscription'
    )


@pytest.mark.django_db
def test_subscriptions_pagination(api_user_client, five_subscriptions):
    data = {'limit': 2}
    response = api_user_client.get(SUBSCRIPTION_LIST_URL, data=data)
    assert 'next' in response.data, (
        'PageNumberPaginator should be used'
    )
    if response.data['next']:
        assert 'limit=' in response.data['next'], (
            'PageNumberPaginator should be overiden with '
            'page_size_query_param="limit"'
        )
    assert len(response.data['results']) == data['limit'], (
        f'Incorrect work of pagination with data={data}'
    )


@pytest.mark.django_db
def test_subscriptions_recipes_pagination(
    api_user_client, subscription, another_user_five_recipes
):
    data = {'recipes_limit': 1}
    response = api_user_client.get(SUBSCRIPTION_LIST_URL, data=data)
    # Test query parameter 'recipes_limit'
    first_author_recipes = response.data['results'][0]['recipes']
    assert len(first_author_recipes) == data['recipes_limit'], (
        'Incorrect work of recipes_limit query parameter '
        f'with data={data}'
    )
    # Test total number author recipes
    assert response.data['results'][0]['recipes_count'] == 5, (
        'Incorrect recipes_count value'
    )
