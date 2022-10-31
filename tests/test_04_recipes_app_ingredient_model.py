from django.db import models


def test_model_name_field(ingredient):
    field = ingredient._meta.get_field('name')
    assert field.max_length == 200, (
        f'Ingredient.{field.name} field should be defiend as max_length=200'
    )
    assert field.db_index, (
        f'Ingredient.{field.name} field should be defiend as db_index=True'
    )
    assert field.unique, (
        f'Ingredient.{field.name} field should be defiend as unique=True'
    )


def test_model_measurement_unit_field(ingredient):
    field = ingredient._meta.get_field('measurement_unit')
    on_delete = models.PROTECT
    related_name = 'ingredients'
    assert field.remote_field.on_delete == on_delete, (
        f'Ingredient.{field.name} field should be defiend as '
        f'on_delete=models.{on_delete.__name__}'
    )
    assert field.remote_field.related_name == related_name, (
        f'Ingredient.{field.name} field should be defiend as '
        f'related_name={related_name}'
    )


def test_models_str_method(ingredient):
    result = f'{ingredient.name} {ingredient.measurement_unit}'
    assert str(ingredient) == result, (
        'Ingredient model __str__() method output is incorrect'
    )
