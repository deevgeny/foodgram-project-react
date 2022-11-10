from django.db import models


def test_model_user_field(shopping_cart):
    field = shopping_cart._meta.get_field('user')
    on_delete = models.CASCADE
    related_name = 'shopping_cart'
    assert field.remote_field.on_delete == on_delete, (
        f'ShoppingCart.{field.name} field should be defined as '
        f'on_delete=models.{on_delete.__name__}'
    )
    assert field.remote_field.related_name == related_name, (
        f'ShoppingCart.{field.name} field should be defined as '
        f'related_name={related_name}'
    )


def test_model_recipe_field(shopping_cart):
    field = shopping_cart._meta.get_field('recipe')
    on_delete = models.CASCADE
    related_name = 'shopping_cart'
    assert field.remote_field.on_delete == on_delete, (
        f'ShoppingCart.{field.name} field should be defined as '
        f'on_delete=models.{on_delete.__name__}'
    )
    assert field.remote_field.related_name == related_name, (
        f'ShoppingCart.{field.name} field should be defined as '
        f'related_name={related_name}'
    )


def test_models_str_method(shopping_cart):
    result = f'{shopping_cart.user} {shopping_cart.recipe}'
    assert str(shopping_cart) == result, (
        'ShoppingCart model __str__() method output is incorrect'
    )
