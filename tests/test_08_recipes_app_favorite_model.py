from django.db import models


def test_user_field(favorite):
    field = favorite._meta.get_field('user')
    assert field.remote_field.on_delete == models.CASCADE, (
        'Favorite.user field should be defined as '
        '`on_delete=models.CASCADE`'
    )
    assert field.remote_field.related_name == 'is_favorited', (
        'Favorite.user field should be defined as '
        '`related_name="is_favorited`'
    )


def test_recipe_field(favorite):
    field = favorite._meta.get_field('recipe')
    assert field.remote_field.on_delete == models.CASCADE, (
        'Favorite.recipe field should be defined as '
        '`on_delete=models.CASCADE`'
    )
    assert field.remote_field.related_name == 'is_favorited', (
        'Favorite.recipe field should be defined as '
        '`related_name="is_favorited`'
    )


def test_models_str_method(favorite):
    result = f'{favorite.user} {favorite.recipe}'
    assert str(favorite) == result, (
        'Favorite model __str__() method output is incorrect'
    )
