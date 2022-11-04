import pytest
from django.core.validators import RegexValidator


@pytest.mark.parametrize('field_name, value',
                         [('name', 200), ('hex_code', 7), ('slug', 200)])
def test_fields_max_length_attribute(tag, field_name, value):
    assert tag._meta.get_field(field_name).max_length == value, (
        f'Tag.{field_name} field should be defined as `max_length={value}`'
    )


@pytest.mark.parametrize('field_name, value',
                         [('name', True), ('hex_code', True), ('slug', True)])
def test_fields_unique_attribute(tag, field_name, value):
    assert tag._meta.get_field(field_name).unique == value, (
        f'Tag.{field_name} field should be defined as `unique={value}`'
    )


@pytest.mark.parametrize('field_name, value',
                         [('name', False), ('hex_code', True), ('slug', True)])
def test_fields_blank_attribute(tag, field_name, value):
    assert tag._meta.get_field(field_name).blank == value, (
        f'Tag.{field_name} field should be defined as `blank={value}`'
    )


@pytest.mark.parametrize('field_name, value',
                         [('name', False), ('hex_code', False),
                          ('slug', True)])
def test_fields_null_attribute(tag, field_name, value):
    assert tag._meta.get_field(field_name).null == value, (
        f'Tag.{field_name} field should be defined as `null={value}`'
    )


def test_hex_code_field_validators(tag):
    field = tag._meta.get_field('hex_code')
    assert type(field.validators[0]) == RegexValidator


def test_model_str_method(tag):
    assert str(tag) == tag.name, (
        'Tag model __str__() method output is incorrect'
    )
