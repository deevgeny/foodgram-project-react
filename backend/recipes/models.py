from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Subscription(models.Model):
    '''Subscription model.'''

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        related_name='subscribed_by'
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('subscriber'),
        related_name='subscribed_to'
    )

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'subscriber'],
                name=('Subscription unique together constraint fields: '
                      'author, subscriber')
            )
        ]

    def __str__(self):
        return f'{self.subscriber} subscribed to {self.author}'


class Tag(models.Model):
    '''Tag model.'''

    name = models.CharField(
        max_length=200,
        verbose_name=_('tag name'),
        unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name=_('HEX color code'),
        unique=True,
        validators=[RegexValidator(regex='^#[0-9A-Fa-f]{6}$')]
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name=_('slug'),
        unique=True,
    )

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


class Unit(models.Model):
    '''Unit of measure model.'''

    name = models.CharField(
        max_length=200,
        verbose_name=_('unit of measure'),
        unique=True
    )

    class Meta:
        verbose_name = _('unit of measure')
        verbose_name_plural = _('units of measure')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    '''Ingredient model.'''

    name = models.CharField(
        max_length=200,
        verbose_name=_('ingredient name'),
        db_index=True,
    )
    measurement_unit = models.ForeignKey(
        Unit,
        verbose_name=_('unit of measure'),
        on_delete=models.PROTECT,
        related_name='ingredients'
    )

    class Meta:
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name=('Ingredient unique together constraint fields: '
                      'name, measurement_unit')
            )
        ]

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class IngredientAmount(models.Model):
    '''Ingredient amount model.'''

    recipe = models.ForeignKey(
        'Recipe',
        verbose_name=_('recipe'),
        on_delete=models.CASCADE,
        related_name='ingredient_amounts'

    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name=_('ingredient'),
        on_delete=models.PROTECT,
        related_name='ingredient_amounts'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name=_('amount'),
        validators=[
            MinValueValidator(1, message=_('Amount should be more than 0'))
        ]
    )

    class Meta:
        verbose_name = _('ingredient amount')
        verbose_name_plural = _('ingredient amounts')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name=('IngredientAmount unique together constraint fields: '
                      'recipe, ingredient')
            )
        ]

    def __str__(self):
        return (f'{self.recipe} {self.ingredient.name} {self.amount} '
                f'{self.ingredient.measurement_unit}')


class Recipe(models.Model):
    '''Recipe model.'''

    author = models.ForeignKey(
        User,
        verbose_name=_('author'),
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        max_length=200,
        verbose_name=_('recipe name')
    )
    image = models.ImageField(
        verbose_name=_('image'),
        upload_to='images/',
    )
    text = models.TextField(
        verbose_name=_('description')
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name=_('ingredients'),
        blank=False,
        related_name='recipes',
        through=IngredientAmount,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('tags'),
        blank=False
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name=_('cooking time'),
        validators=[
            MinValueValidator(
                1, message=_('Cooking time should be more than 0')
            )
        ]
    )

    class Meta:
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')
        ordering = ('id', )

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    '''Recipe shopping cart model.'''

    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_('recipe'),
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        verbose_name = _('shopping cart')
        verbose_name_plural = _('shopping carts')

    def __str__(self):
        return f'{self.user} {self.recipe}'


class Favorite(models.Model):
    '''Favorite recipes model.'''

    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_('recipe'),
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    class Meta:
        verbose_name = _('favorite')
        verbose_name_plural = _('favorites')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name=('Favorite unique together constraint fields: '
                      'user, recipe')
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'
