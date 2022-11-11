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
def five_tags(db):
    tag_names = ['one', 'two', 'tree', 'four', 'five']
    colors = ['#111111', '#222222', '#333333', '#444444', '#555555']
    tags = []

    for i in range(len(tag_names)):
        tags.append(Tag.objects.create(name=tag_names[i], color=colors[i],
                                       slug=tag_names[i]))
    return tags
