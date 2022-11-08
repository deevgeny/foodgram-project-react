from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from recipes.models import Ingredient, IngredientsList, Recipe, Tag
from rest_framework import serializers

User = get_user_model()


class CustomUserReadSerializer(serializers.ModelSerializer):
    '''User model serializer to display user info.'''

    is_subscribed = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')
        read_only_fields = ('email', 'id', 'username', 'first_name',
                            'last_name', 'is_subscribed')


class CustomUserCreateSerializer(UserCreateSerializer):
    '''Djoser customized serializer for registration of new users.'''

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'first_name',
                  'last_name', 'password')
        read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    '''Tag model serializer.'''

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    '''Ingredient model serializer.'''

    measurement_unit = serializers.StringRelatedField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientsListSerializer(serializers.ModelSerializer):
    '''IngredientsList model serializer.'''

    name = serializers.StringRelatedField(read_only=True, source='item.name')
    measurement_unit = serializers.StringRelatedField(
        read_only=True, source='item.measurement_unit'
    )

    class Meta:
        model = IngredientsList
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    '''Recipe model read serializer.'''

    author = CustomUserReadSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientsListSerializer(read_only=True, many=True)
    is_favorited = serializers.BooleanField(read_only=True, default=False)
    is_in_shopping_cart = serializers.BooleanField(read_only=True,
                                                   default=False)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
        read_only_fields = ('id',)


class RecipeCreateSerializer(serializers.ModelSerializer):
    '''Recipe model create serializer.'''

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'ingredients', 'name', 'image', 'text',
                  'cooking_time')
        read_only_fields = ('author',)
