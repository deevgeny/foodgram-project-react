from django.db import models


def test_author_field(recipe):
    field = recipe._meta.get_field('author')
    assert field.remote_field.on_delete == models.CASCADE, (
        'Recipe.author field should be defined as `on_delete=models.CASCADE`'
    )
    assert field.remote_field.related_name == 'recipes', (
        'Recipe.author field should be defined as `related_name="recipes"`'
    )


def test_name_field(recipe):
    field = recipe._meta.get_field('name')
    assert field.max_length == 200, (
        'Recipe.name field should be defined as `max_length=200`'
    )


def test_image_field(recipe):
    field = recipe._meta.get_field('image')
    assert field.upload_to == 'recipes/', (
        'Recipe.image field should be defined as `upload_to="recipe/"`'
    )
    assert field.blank, (
        'Recipe.image field should be defined as `blank=True`'
    )


def test_text_field(recipe):
    field = recipe._meta.get_field('text')
    assert not field.blank, (
        'Recipe.text field should be defined as `blank=False`'
    )


def test_ingredients_field(recipe):
    field = recipe._meta.get_field('ingredients')
    assert type(field) == models.ManyToManyField, (
        'Recipe.ingredients field should be `ManyToManyField` type'
    )


def test_tag_field(recipe):
    field = recipe._meta.get_field('tags')
    assert type(field) == models.ManyToManyField, (
        'Recipe.tag field should be `ManyToManyField` type'
    )


def test_cooking_time_field(recipe):
    field = recipe._meta.get_field('cooking_time')
    assert type(field) == models.PositiveSmallIntegerField, (
        'Recipe.cooking_time field should be `PositiveSmallIntegerField` type'
    )


def test_models_str_method(recipe):
    assert str(recipe) == recipe.name, (
        'Recipe model __str__() method output is incorrect'
    )


def test_models_meta_class_attributes(recipe):
    assert recipe._meta.ordering == ('-id',), (
        'Recipe model `class Meta` should have `ordering=("-id",)`'
    )
