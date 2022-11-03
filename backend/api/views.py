# from django.shortcuts import render
from djoser.views import UserViewSet

from .serializers import CustomUserSerializer


class CustomUserViewset(UserViewSet):
    serializer_class = CustomUserSerializer
