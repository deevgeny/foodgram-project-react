from django.core.validators import MinValueValidator
from django.db import models


def test_model_recipe_field(ingredient_amount):
    field = ingredient_amount._meta.get_field('recipe')
    on_delete = models.CASCADE
    related_name = 'ingredient_amounts'
    assert field.remote_field.on_delete == on_delete, (
        f'IngredientAmount.{field.name} field should be defiend as '
        f'on_delete=models.{on_delete.__name__}'
    )
    assert field.remote_field.related_name == related_name, (
        f'IngredientAmount.{field.name} field should be defiend as '
        f'related_name={related_name}'
    )


def test_model_ingredient_field(ingredient_amount):
    field = ingredient_amount._meta.get_field('ingredient')
    on_delete = models.PROTECT
    related_name = 'ingredient_amounts'
    assert field.remote_field.on_delete == on_delete, (
        f'IngredientAmount.{field.name} field should be defiend as '
        f'on_delete=models.{on_delete.__name__}'
    )
    assert field.remote_field.related_name == related_name, (
        f'IngredientAmount.{field.name} field should be defiend as '
        f'related_name={related_name}'
    )


def test_model_amount_field(ingredient_amount):
    field = ingredient_amount._meta.get_field('amount')
    field_type = models.PositiveSmallIntegerField
    validator = MinValueValidator
    limit_value = 1
    assert type(field) == field_type, (
        f'IngredientAmount.{field.name} field should be {field_type.__name__} '
        ' type'
    )
    assert isinstance(field.validators[0], validator), (
        f'IngredientAmount.{field.name} field shold have {validator.__name__}'
    )
    assert field.validators[0].limit_value == limit_value, (
        f'IngredientAmount.{field.name} field {validator.__name__} should be '
        f'defined as limit_value={limit_value}'
    )


def test_model_meta_class_constraints(ingredient_amount):
    constraint = models.UniqueConstraint
    assert len(ingredient_amount._meta.constraints) == 1, (
        'IngredientAmount model class Meta should have constraints'
    )
    assert isinstance(ingredient_amount._meta.constraints[0], constraint), (
        f'IngredientAmount model class Meta should have {constraint}'
    )


def test_model_meta_class_constraints_fields(ingredient_amount):
    fields = ('recipe', 'ingredient')
    assert ingredient_amount._meta.constraints[0].fields == fields, (
        'IngredientAmount model class Meta should have unique constraint for '
        f'{fields} model fields'
    )


def test_models_str_method(ingredient_amount):
    result = (
        f'{ingredient_amount.recipe} {ingredient_amount.ingredient.name} '
        f'{ingredient_amount.amount} '
        f'{ingredient_amount.ingredient.measurement_unit}'
    )
    assert str(ingredient_amount) == result, (
        'IngredientAmount model __str__() method output is incorrect'
    )
