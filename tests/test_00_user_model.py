import pytest
from django.contrib.auth import get_user_model


class Test00UserModel:

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize('field_name, result',
                             (['email', True], ['username', True]))
    def test_fields_unique_attribute(self, user, field_name, result):
        assert user._meta.get_field(field_name).unique == result, (
            f'User.{field_name} field should be defined as `unique={result}`'
        )

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize('field_name, result',
                             (['username', False], ['email', False], ['first_name', False],
                              ['last_name', False]))
    def test_fields_blank_attribute(self, user, field_name, result):
        assert user._meta.get_field(field_name).blank == result, (
            f'User.{field_name} field should be defined as `blank={result}`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_fixture_load(self, django_db_setup):
        x = get_user_model().objects.filter(username="simple_user").count()
        assert x == 1
