from django.core.validators import MaxLengthValidator, MinValueValidator
from django.db import models

from recipes.models import IngredientAmount


def test_model_author_field(recipe):
    field = recipe._meta.get_field('author')
    on_delete = models.CASCADE
    related_name = 'recipes'
    assert field.remote_field.on_delete == on_delete, (
        f'Recipe.{field.name} field should be defined as '
        f'on_delete=models.{on_delete.__name__}'
    )
    assert field.remote_field.related_name == related_name, (
        f'Recipe.{field.name} field should be defined as '
        f'related_name={related_name}'
    )


def test_model_name_field(recipe):
    field = recipe._meta.get_field('name')
    max_length = 200
    assert field.max_length == max_length, (
        f'Recipe.{field.name} field should be defined as '
        f'max_length={max_length}'
    )


def test_model_image_field(recipe):
    field = recipe._meta.get_field('image')
    upload_to = 'images/'
    blank = False
    assert field.upload_to == upload_to, (
        f'Recipe.{field.name} field should be defined as '
        f'upload_to={upload_to}'
    )
    assert field.blank == blank, (
        f'Recipe.{field.name} field should be defined as blank={blank}'
    )


def test_model_text_field(recipe):
    field = recipe._meta.get_field('text')
    blank = False
    validator = MaxLengthValidator
    limit_value = 1000
    assert field.blank == blank, (
        f'Recipe.{field.name} field should be defined as blank={blank}'
    )
    assert isinstance(field.validators[0], validator), (
        f'Recipe.{field.name} field should have {validator.__name__}'
    )
    assert field.validators[0].limit_value == limit_value, (
        f'Recipe.{field.name} field {validator.__name__} should be '
        f'defined as limit_value={limit_value}'
    )


def test_model_ingredients_field(recipe):
    field = recipe._meta.get_field('ingredients')
    field_type = models.ManyToManyField
    related_name = 'recipes'
    through = IngredientAmount
    assert isinstance(field, field_type), (
        f'Recipe.{field.name} field should be {field_type.__name__} type'
    )
    assert field.remote_field.related_name == related_name, (
        f'Recipe.{field.name} field should be defined as '
        f'related_name={related_name}'
    )
    assert field.remote_field.through == through, (
        f'Recipe.{field.name} field should be defined as '
        f'through={through.__name__}'
    )


def test_model_tag_field(recipe):
    field = recipe._meta.get_field('tags')
    field_type = models.ManyToManyField
    assert isinstance(field, field_type), (
        f'Recipe.{field.name} field should be {field_type.__name__} type'
    )


def test_model_cooking_time_field(recipe):
    field = recipe._meta.get_field('cooking_time')
    field_type = models.PositiveSmallIntegerField
    validator = MinValueValidator
    limit_value = 1
    assert isinstance(field, field_type), (
        f'Recipe.{field.name} field should be {field_type.__name__} type'
    )
    assert isinstance(field.validators[0], validator), (
        f'Recipe.{field.name} field should have {validator.__name__}'
    )
    assert field.validators[0].limit_value == limit_value, (
        f'Recipe.{field.name} field {validator.__name__} should be '
        f'defined as limit_value={limit_value}'
    )


def test_models_str_method(recipe):
    assert str(recipe) == recipe.name, (
        'Recipe model __str__() method output is incorrect'
    )


def test_models_meta_class_attributes(recipe):
    ordering = ('id',)
    assert recipe._meta.ordering == ordering, (
        f'Recipe model class Meta should have ordering={ordering}'
    )
