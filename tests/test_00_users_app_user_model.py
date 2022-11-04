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
def test_fields_blank_attribute(user, field_name, result):
    assert user._meta.get_field(field_name).blank == result, (
        f'User.{field_name} field should be defined as `blank={result}`'
    )


def test_user_login_field():
    assert User.USERNAME_FIELD == 'username', (
        'Incorrect User.USERNAME_FIELD'
    )
