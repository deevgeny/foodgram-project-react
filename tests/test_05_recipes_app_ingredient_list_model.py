from django.db import models


def test_ingredient_field(ingredient_amount):
    field = ingredient_amount._meta.get_field('ingredient')
    assert field.remote_field.on_delete == models.CASCADE, (
        'IngredientAmount.ingredient field should be defiend as ',
        '`on_delete=models.CASCADE`'
    )
    assert field.remote_field.related_name == 'ingredient_amounts', (
        'IngredientAmount.item field should be defiend as ',
        '`related_name="ingredients_list"`'
    )


def test_amount_field(ingredient_amount):
    field = ingredient_amount._meta.get_field('amount')
    assert type(field) == models.PositiveSmallIntegerField, (
        'IngredientAmount.amount field should be `PositiveSmallIntegerField` '
        ' type'
    )


def test_models_str_method(ingredient_amount):
    result = f'{ingredient_amount.item} {ingredient_amount.amount}'
    assert str(ingredient_amount) == result, (
        'IngredientAmount model __str__() method output is incorrect'
    )
