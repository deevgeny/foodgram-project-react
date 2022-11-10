from django.db import models


def test_model_user_field(favorite):
    field = favorite._meta.get_field('user')
    on_delete = models.CASCADE
    related_name = 'favorites'
    assert field.remote_field.on_delete == on_delete, (
        f'Favorite.{field.name} field should be defined as '
        f'on_delete=models.{on_delete.__name__}'
    )
    assert field.remote_field.related_name == related_name, (
        f'Favorite.{field.name} field should be defined as '
        f'related_name={related_name}'
    )


def test_model_recipe_field(favorite):
    field = favorite._meta.get_field('recipe')
    on_delete = models.CASCADE
    related_name = 'favorited_by'
    assert field.remote_field.on_delete == on_delete, (
        f'Favorite.{field.name} field should be defined as '
        f'`on_delete=models.{on_delete.__name__}`'
    )
    assert field.remote_field.related_name == related_name, (
        f'Favorite.{field.name} field should be defined as '
        f'related_name={related_name}`'
    )


def test_model_meta_class_constraints(favorite):
    constraint = models.UniqueConstraint
    assert len(favorite._meta.constraints) == 1, (
        'Favorite model class Meta should have constraints'
    )
    assert isinstance(favorite._meta.constraints[0], constraint), (
        f'Favorite model class Meta should have {constraint}'
    )


def test_model_meta_class_constraints_fields(favorite):
    fields = ('user', 'recipe')
    assert favorite._meta.constraints[0].fields == fields, (
        'Favorite model class Meta should have unique constraint for '
        f'{fields} model fields'
    )


def test_models_str_method(favorite):
    result = f'{favorite.user} {favorite.recipe}'
    assert str(favorite) == result, (
        'Favorite model __str__() method output is incorrect'
    )
