import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from recipes.models import Ingredient, Unit

DATA_PATH = settings.BASE_DIR.joinpath('data')


class Command(BaseCommand):
    '''Custom command to load ingredients to database.'''

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='?', default='ingredients.json',
                            type=str)

    def handle(self, *args, **options):
        try:
            filepath = DATA_PATH / options['file']
            with open(filepath, 'r') as f:
                data = json.load(f)

            # Collect measurement unit data
            uom = set()
            for i in data:
                uom.add(i['measurement_unit'])

            # Reorganize ingredients data {'measurement_unit': ['name', ...]}
            uom_product = {}
            for i in data:
                if i['measurement_unit'] in uom_product:
                    uom_product[i['measurement_unit']].append(i['name'])
                else:
                    uom_product[i['measurement_unit']] = [i['name']]

            # Create units in database
            units = []
            for name in uom:
                units.append(Unit.objects.get_or_create(name=name))
                self.stdout.write(
                    self.style.SUCCESS(
                        'Unit "%s" was added to database' % name
                    )
                )

            # Create ingredients in database
            for unit in units:
                for ingredient in uom_product[unit[0].name]:
                    Ingredient.objects.get_or_create(
                        name=ingredient,
                        measurement_unit=unit[0]
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            ('Ingredient "%s" was added to database'
                             % ingredient)
                        )
                    )
        except FileNotFoundError:
            raise CommandError('File "%s" not found' % filepath)
