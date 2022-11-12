import pytest
from recipes.models import Unit


@pytest.fixture
def unit(db):
    return Unit.objects.create(name='kg')


@pytest.fixture
def five_units(db):
    names = ['kg', 'gr', 'pcs', 'ltr', 'cup']
    units = []
    for name in names:
        units.append(Unit.objects.create(name=name))
    return units
