from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Ingredient, IngredientsList, Recipe, Tag
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    '''Custom serializer for user model.'''

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class CustomUserCreateSerializer(UserCreateSerializer):
    '''Custom serializer for registration of new users.'''

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


class RecipeSerializer(serializers.ModelSerializer):
    '''Recipe model serializer.'''
    author = CustomUserCreateSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientsListSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time')
