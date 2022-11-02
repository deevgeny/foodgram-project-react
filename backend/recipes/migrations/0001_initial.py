# Generated by Django 3.2 on 2022-11-01 16:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200,
                 unique=True, verbose_name='tag name')),
                ('hex_code', models.CharField(blank=True, max_length=7, unique=True, validators=[
                 django.core.validators.RegexValidator(regex='^#[0-9A-Fa-f]{6}$')], verbose_name='HEX color code')),
                ('slug', models.SlugField(blank=True, max_length=200,
                 null=True, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='subscribers', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='subscriber')),
            ],
            options={
                'verbose_name': 'subscription',
                'verbose_name_plural': 'subscriptions',
            },
        ),
    ]
