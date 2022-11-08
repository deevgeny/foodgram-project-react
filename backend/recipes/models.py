from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Subscription(models.Model):
    '''Subscription model.'''

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        related_name='subscribers'
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('subscriber'),
        related_name='subscriptions'
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
        unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name=_('HEX color code'),
        unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(regex='^#[0-9A-Fa-f]{6}$')]
    )
    slug = models.SlugField(
        max_length=200,
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
        db_index=True,
        unique=True
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

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class IngredientsList(models.Model):
    '''Ingredients list model.'''

    item = models.ForeignKey(
        Ingredient,
        verbose_name=_('item'),
        on_delete=models.CASCADE,
        related_name='ingredients_list'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name=_('amount')
    )

    class Meta:
        verbose_name = _('ingredients list')
        verbose_name_plural = _('ingredients lists')

    def __str__(self):
        return f'{self.item} {self.amount}'


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
        upload_to='recipes/',
        blank=True
    )
    text = models.TextField(
        verbose_name=_('description')
    )
    ingredients = models.ManyToManyField(
        IngredientsList,
        verbose_name=_('ingredients'),
        blank=False
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('tags'),
        blank=False
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name=_('cooking time')
    )

    class Meta:
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')
        ordering = ('-id', )

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        for ingredient in self.ingredients:
            ingredient.objects.delete()
        super(Recipe, self).delete(*args, **kwargs)


class ShoppingCart(models.Model):
    '''Recipe shopping cart model.'''

    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='my_shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_('recipe'),
        on_delete=models.CASCADE,
        related_name='all_shopping_carts'
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
        related_name='favorited_recipes'
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

    def __str__(self):
        return f'{self.user} {self.recipe}'
