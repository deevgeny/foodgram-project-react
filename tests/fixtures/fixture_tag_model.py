import pytest
from recipes.models import Tag


@pytest.fixture
def tag(db):
    return Tag.objects.create(
        name='tasty snack',
        color='#000000',
        slug='tasty_snack'
    )


@pytest.fixture
def create_five_tags(db):
    tags = ['one', 'two', 'tree', 'four', 'five']
    for tag in tags:
        Tag.objects.create(
            name=tag,
            slug=tag
        )
