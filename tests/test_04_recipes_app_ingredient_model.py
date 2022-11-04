from django.db import models


def test_name_field(ingredient):
    field = ingredient._meta.get_field('name')
    assert field.max_length == 200, (
        'Ingredient.name field should be defiend as `max_length=200`'
    )
    assert field.db_index, (
        'Ingredient.name field should be defiend as `db_index=True`'
    )
    assert field.unique, (
        'Ingredient.name field should be defiend as `unique=True`'
    )


def test_measurement_unit_field(ingredient):
    field = ingredient._meta.get_field('measurement_unit')
    assert field.remote_field.on_delete == models.PROTECT, (
        'Ingredient.measurement_unit field should be defiend as '
        '`on_delete=models.CASCADE`'
    )
    assert field.remote_field.related_name == 'ingredients', (
        'Ingredient.measurement_unit field should be defiend as '
        '`related_name="ingredients"`'
    )


def test_models_str_method(ingredient):
    result = f'{ingredient.name} {ingredient.measurement_unit}'
    assert str(ingredient) == result, (
        'Ingredient model __str__() method output is incorrect'
    )
