import pytest
from django.core.management import call_command

@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(
        username='TestUser', email='testuser@fg.fake', first_name='Misha',
        last_name='Pupkin'
        )

@pytest.fixture
def superuser(django_user_model):
    return django_user_model.objects.create(
        username='SuperUser', email='superuser@fg.fake', first_name='Kolya',
        last_name='Bublikov'
    )

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
   with django_db_blocker.unblock():
       call_command('loaddata', 'tests/fixture.json')