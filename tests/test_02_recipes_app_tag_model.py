import pytest
from django.core.validators import RegexValidator


@pytest.mark.parametrize('field_name, value',
                         [('name', 200), ('color', 7), ('slug', 200)])
def test_model_fields_max_length_attribute(tag, field_name, value):
    assert tag._meta.get_field(field_name).max_length == value, (
        f'Tag.{field_name} field should be defined as max_length={value}'
    )


@pytest.mark.parametrize('field_name, value',
                         [('name', True), ('color', True), ('slug', True)])
def test_model_fields_unique_attribute(tag, field_name, value):
    assert tag._meta.get_field(field_name).unique == value, (
        f'Tag.{field_name} field should be defined as unique={value}'
    )


@pytest.mark.parametrize('field_name, value',
                         [('name', False), ('color', False), ('slug', False)])
def test_model_fields_blank_attribute(tag, field_name, value):
    assert tag._meta.get_field(field_name).blank == value, (
        f'Tag.{field_name} field should be defined as blank={value}'
    )


@pytest.mark.parametrize('field_name, value',
                         [('name', False), ('color', False),
                          ('slug', False)])
def test_model_fields_null_attribute(tag, field_name, value):
    assert tag._meta.get_field(field_name).null == value, (
        f'Tag.{field_name} field should be defined as null={value}'
    )


def test_hex_code_field_validator(tag):
    field = tag._meta.get_field('color')
    validator = RegexValidator
    assert isinstance(field.validators[0], validator), (
        f'Tag.{field.name} field shold have {validator.__name__}'
    )


@pytest.mark.parametrize('field_name, value',
                         [('name', True), ('color', False),
                          ('slug', True)])
def test_model_fields_db_index_attribute(tag, field_name, value):
    assert tag._meta.get_field(field_name).db_index == value, (
        f'Tag.{field_name} field should be defined as db_index={value}'
    )



def test_model_str_method(tag):
    assert str(tag) == tag.name, (
        'Tag model __str__() method output is incorrect'
    )
