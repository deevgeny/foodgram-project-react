import pytest
from django.db import models


@pytest.mark.parametrize('field_name, value',
                         [('author', models.CASCADE),
                          ('subscriber', models.CASCADE)])
def test_model_fields_on_delete_attribute(subscription, field_name, value):
    assert subscription._meta.get_field(
        field_name).remote_field.on_delete == value, (
        f'Subscription.{field_name} field should be defined as '
        f'on_delete=models.{value.__name__}'
    )


@pytest.mark.parametrize('field_name, value',
                         [('author', 'subscribed_by'),
                          ('subscriber', 'subscribed_to')])
def test_model_fields_related_name_attribute(subscription, field_name, value):
    assert subscription._meta.get_field(
        field_name).remote_field.related_name == value, (
        f'Subscription.{field_name} field should be defined as '
        f'related_name={value}'
    )


def test_model_meta_class_constraints(subscription):
    constraint = models.UniqueConstraint
    assert len(subscription._meta.constraints) == 1, (
        'Subscription model class Meta should have constraints'
    )
    assert isinstance(subscription._meta.constraints[0], constraint), (
        f'Subscription model class Meta should have {constraint}'
    )


def test_model_meta_class_constraints_fields(subscription):
    fields = ('author', 'subscriber')
    assert subscription._meta.constraints[0].fields == fields, (
        'Subscription model class Meta should have unique constraint for '
        f'{fields} model fields'
    )


def test_model_str_method(subscription):
    result = f'{subscription.subscriber} subscribed to {subscription.author}'
    assert str(subscription) == result, (
        'Subscription model __str__() method output is incorrect'
    )
