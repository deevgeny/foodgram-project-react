import pytest
from django.db import models


@pytest.mark.parametrize('field_name, value',
                         [('author', models.CASCADE),
                          ('subscriber', models.CASCADE)])
def test_fields_on_delete_attribute(subscription, field_name, value):
    assert subscription._meta.get_field(
        field_name).remote_field.on_delete == value, (
        f'Subscription.{field_name} field should be defined as '
        f'`on_delete=models.{value.__name__}`'
    )


@pytest.mark.parametrize('field_name, value',
                         [('author', 'subscribers'),
                          ('subscriber', 'subscriptions')])
def test_fields_related_name_attribute(subscription, field_name, value):
    assert subscription._meta.get_field(
        field_name).remote_field.related_name == value, (
        f'Subscription.{field_name} field should be defined as '
        f'`related_name={value}`'
    )


def test_model_str_method(subscription):
    result = f'{subscription.subscriber} subscribed to {subscription.author}'
    assert str(subscription) == result, (
        'Subscription model __str__() method output is incorrect'
    )
