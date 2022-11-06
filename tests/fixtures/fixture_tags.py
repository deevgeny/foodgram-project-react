import pytest
from recipes.models import Tag


@pytest.fixture
def create_five_tags(db):
    tags = ['one', 'two', 'tree', 'four', 'five']
    for tag in tags:
        Tag.objects.create(
            name=tag,
            slug=tag
        )
