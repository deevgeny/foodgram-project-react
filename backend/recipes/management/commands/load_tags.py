import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from recipes.models import Tag

DATA_PATH = settings.BASE_DIR / 'data'


class Command(BaseCommand):
    """Custom command to load tags to database."""

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='?', default='tags.json',
                            type=str)

    def handle(self, *args, **options):
        try:
            filepath = DATA_PATH / options['file']
            with open(filepath, 'r') as f:
                data = json.load(f)

            # Create tags in database
            for tag in data:
                Tag.objects.get_or_create(
                    name=tag['name'],
                    color=tag['color'],
                    slug=tag['slug']
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        'Tag "%s" was added to database' % tag['name']
                    )
                )
        except FileNotFoundError:
            raise CommandError('File "%s" not found' % filepath)
