from django.db import models


def test_user_field(favorite):
    field = favorite._meta.get_field('user')
    on_delete = models.CASCADE
    related_name = 'favorited_recipes'
    assert field.remote_field.on_delete == on_delete, (
        'Favorite.user field should be defined as '
        '`on_delete=models.CASCADE`'
    )
    assert field.remote_field.related_name == related_name, (
        'Favorite.user field should be defined as '
        f'`related_name={related_name}`'
    )


def test_recipe_field(favorite):
    field = favorite._meta.get_field('recipe')
    on_delete = models.CASCADE
    related_name = 'favorited_by'
    assert field.remote_field.on_delete == on_delete, (
        'Favorite.recipe field should be defined as '
        f'`on_delete=models.{on_delete.__name__}`'
    )
    assert field.remote_field.related_name == related_name, (
        'Favorite.recipe field should be defined as '
        f'`related_name={related_name}`'
    )


def test_models_str_method(favorite):
    result = f'{favorite.user} {favorite.recipe}'
    assert str(favorite) == result, (
        'Favorite model __str__() method output is incorrect'
    )
