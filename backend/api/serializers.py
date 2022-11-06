from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Tag
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
        fields = ('id', 'name', 'hex_code', 'slug')
        read_only_fields = ('id',)
