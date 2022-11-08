from http import HTTPStatus

import pytest

TAG_URL = '/api/tags/'


@pytest.mark.django_db
def test_urls_availability(api_client, create_five_tags):
    response = api_client.get(TAG_URL)
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {TAG_URL} not found'
    )
    response = api_client.get(TAG_URL + '1/')
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'URL {TAG_URL + "1/"} not found'
    )


@pytest.mark.django_db
def test_urls_unauthenticated_permissions(api_client, create_five_tags):
    response = api_client.get(TAG_URL)
    assert response.status_code == HTTPStatus.OK, (
        f'GET request to {TAG_URL} should be available for all users'
    )
    response = api_client.get(TAG_URL + '1/')
    assert response.status_code == HTTPStatus.OK, (
        f'GET request to {TAG_URL +"1/"} should be available for all users'
    )


@pytest.mark.django_db
def test_tags_have_no_pagination(api_client, create_five_tags):
    response = api_client.get(TAG_URL)
    assert 'count' not in response.data, (
        f'URL {TAG_URL} should not have pagination'
    )


@pytest.mark.django_db
def test_api_response_fields(api_client, create_five_tags):
    fields = ['id', 'name', 'color', 'slug']
    response = api_client.get(TAG_URL + '1/')
    assert len(response.data) == len(fields), (
        f'Tag model api response should have {len(fields)} fields'
    )
    for field in fields:
        assert field in response.data, (
            f'Field name `{field}` is missing or incorrect in Tag model '
            'api response'
        )


@pytest.mark.django_db
def test_tag_not_found(api_client):
    response = api_client.get(TAG_URL + '1/')
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        f'Incorrect response status code {response.status_code} '
        'for not existing tag'
    )
