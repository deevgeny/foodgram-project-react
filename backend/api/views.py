from django.shortcuts import get_object_or_404
from djoser import utils
from djoser.conf import settings
from djoser.views import TokenCreateView
from recipes.models import Ingredient, IngredientsList, Recipe, Tag
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer,
    TagSerializer,
)


class CustomTokenCreateView(TokenCreateView):
    '''Custom Token create view.

    Override response status code from 200_OK to 201_CREATED.
    '''

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data,
            status=status.HTTP_201_CREATED
        )


class ReadOnlyNoPaginationModelViewSet(ReadOnlyModelViewSet):
    '''Base ModelViewSet class with predifined permissions and pagination.'''

    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class TagViewSet(ReadOnlyNoPaginationModelViewSet):
    '''Tag model viewset.'''

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyNoPaginationModelViewSet):
    '''Ingredient model viewset.'''

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    '''Recipe model viewset.'''

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        '''Override perform_create method.

        * Add self.request.user to serializer author field before saving.
        * Return saved model instance for customized response.
        '''
        return serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        '''Override create method.

        * Create ingredients and add to new recipe record.
        * Return custom response data with RecipeReadSerializer.
        '''
        # Create ingredients and add ids to request data
        ingredients = []
        for item in request.data.get('ingredients'):
            ingredient = get_object_or_404(Ingredient, id=item['id'])
            obj = IngredientsList.objects.create(
                item=ingredient, amount=item['amount']
            )
            ingredients.append(obj.id)
        request.data['ingredients'] = ingredients

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Prepare custom response data
        response_serializer = RecipeReadSerializer(recipe)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED,
            headers=headers
        )
