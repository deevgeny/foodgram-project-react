from django.db import models


def test_user_field(shopping_cart):
    field = shopping_cart._meta.get_field('user')
    assert field.remote_field.on_delete == models.CASCADE, (
        'ShoppingCart.user field should be defined as '
        '`on_delete=models.CASCADE`'
    )
    assert field.remote_field.related_name == 'my_shopping_cart', (
        'ShoppingCart.user field should be defined as '
        '`related_name="my_shopping_cart`'
    )


def test_recipe_field(shopping_cart):
    field = shopping_cart._meta.get_field('recipe')
    assert field.remote_field.on_delete == models.CASCADE, (
        'ShoppingCart.recipe field should be defined as '
        '`on_delete=models.CASCADE`'
    )
    assert field.remote_field.related_name == 'all_shopping_carts', (
        'ShoppingCart.recipe field should be defined as '
        '`related_name="all_shopping_carts`'
    )


def test_models_str_method(shopping_cart):
    result = f'{shopping_cart.user} {shopping_cart.recipe}'
    assert str(shopping_cart) == result, (
        'ShoppingCart model __str__() method output is incorrect'
    )
