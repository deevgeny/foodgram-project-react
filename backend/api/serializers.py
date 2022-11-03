from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer

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
        fields = ('email', 'username', 'first_name', 'first_name', 'last_name',
                  'password')
