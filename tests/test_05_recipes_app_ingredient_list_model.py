from django.db import models


def test_item_field(ingredients_list):
    field = ingredients_list._meta.get_field('item')
    assert field.remote_field.on_delete == models.CASCADE, (
        'IngredientsList.item field should be defiend as ',
        '`on_delete=models.CASCADE`'
    )
    assert field.remote_field.related_name == 'ingredients_list', (
        'IngredientsList.item field should be defiend as ',
        '`related_name="ingredients_list"`'
    )


def test_amount_field(ingredients_list):
    field = ingredients_list._meta.get_field('amount')
    assert type(field) == models.PositiveSmallIntegerField, (
        'IngredientsList.amount field should be `PositiveSmallIntegerField` '
        ' type'
    )


def test_models_str_method(ingredients_list):
    result = f'{ingredients_list.item} {ingredients_list.amount}'
    assert str(ingredients_list) == result, (
        'IngredientsList model __str__() method output is incorrect'
    )
