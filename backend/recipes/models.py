import re

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Subscriptions(models.Model):
    '''Subscription model.'''

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        related_name='subscribers',
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('subscriber'),
        related_name='subscriptions',
    )

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')

    def __str__(self):
        return f'{self.subscriber} subscribed to {self.author}'


class Tag(models.Model):
    '''Tag model.'''

    name = models.CharField(
        max_length=200,
        verbose_name=_('tag name'),
        unique = True,
    )
    hex_code = models.CharField(
        max_length=7,
        verbose_name=_('HEX color code'),
        unique=True,
        blank=True,
        validators=[RegexValidator(regex='^#[0-9A-Fa-f]{6}$')]
    )
    slug = models.SlugField(
        max_length = 200,
        verbose_name=_('slug'),
        unique=True,
        blank=True,
        null=True

    )

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
    
    def __str__(self):
        return self.name
