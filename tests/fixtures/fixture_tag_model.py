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
    colors = ['#111111', '#222222', '#333333', '#444444', '#555555']

    for i in range(len(tags)):
        Tag.objects.create(
            name=tags[i],
            color=colors[i],
            slug=tags[i]
        )
