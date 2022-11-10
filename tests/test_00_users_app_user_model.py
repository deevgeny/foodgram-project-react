import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.parametrize('field_name, result',
                         (['email', True], ['username', True]))
def test_fields_unique_attribute(user, field_name, result):
    assert user._meta.get_field(field_name).unique == result, (
        f'User.{field_name} field should be defined as `unique={result}`'
    )


@pytest.mark.parametrize('field_name, result',
                         (['username', False], ['email', False],
                          ['first_name', False], ['last_name', False]))
def test_model_fields_blank_attribute(user, field_name, result):
    assert user._meta.get_field(field_name).blank == result, (
        f'User.{field_name} field should be defined as `blank={result}`'
    )


def test_model_user_login_field():
    username_field = 'username'
    assert User.USERNAME_FIELD == username_field, (
        'User.USERNAME_FIELD should be defined as '
        f'USERNAME_FIELD = {username_field}'
    )


def test_model_meta_class_ordering(user):
    ordering = ('id',)
    assert user._meta.ordering == ordering, (
        f'User model class Meta should have ordering={ordering}'
    )
