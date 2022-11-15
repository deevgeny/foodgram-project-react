from django.db import models


def test_model_name_field(ingredient):
    field = ingredient._meta.get_field('name')
    assert field.max_length == 200, (
        f'Ingredient.{field.name} field should be defiend as max_length=200'
    )
    assert field.db_index, (
        f'Ingredient.{field.name} field should be defiend as db_index=True'
    )
    assert not field.unique, (
        f'Ingredient.{field.name} field should be defiend as unique=False'

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


def test_model_meta_class_constraints(ingredient):
    constraint = models.UniqueConstraint
    assert len(ingredient._meta.constraints) == 1, (
        'Ingredient model class Meta should have constraints'
    )
    assert isinstance(ingredient._meta.constraints[0], constraint), (
        f'Ingredient model class Meta should have {constraint}'
    )


def test_model_meta_class_constraints_fields(ingredient):
    fields = ('name', 'measurement_unit')
    assert ingredient._meta.constraints[0].fields == fields, (
        'Ingredient model class Meta should have unique constraint for '
        f'{fields} model fields'
    )



def test_models_str_method(ingredient):
    result = f'{ingredient.name} {ingredient.measurement_unit}'
    assert str(ingredient) == result, (
        'Ingredient model __str__() method output is incorrect'
    )
