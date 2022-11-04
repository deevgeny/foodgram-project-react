

def test_fields_max_length_attribute(unit):
    assert unit._meta.get_field('name').max_length == 200, (
        'Unit.name field should be defined as `max_length=200`'
    )


def test_fields_unique_attribute(unit):
    assert unit._meta.get_field('name').unique, (
        'Unit.name field should be defined as `unique=True`'
    )


def test_models_str_method(unit):
    assert str(unit) == unit.name, (
        'Unit model __str__() method output is incorrect'
    )
