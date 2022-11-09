from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser import utils
from djoser.conf import settings
from djoser.views import TokenCreateView
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingCart,
    Subscription,
    Tag,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientSearchFilter, RecipeFilter
from .paginator import CustomPageNumberPagination
from .permissions import IsAuthorIsAdminOrReadOnly
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeListSerializer,
    ShoppingCartSerializer,
    SubscriptionSerializer,
    TagSerializer,
)

User = get_user_model()


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


class TagViewSet(ReadOnlyModelViewSet):
    '''Tag model viewset.'''

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    '''Ingredient model viewset.'''

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = [IngredientSearchFilter]
    search_field = ('^name',)


class RecipeViewSet(ModelViewSet):
    '''Recipe model viewset.'''

    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorIsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeCreateSerializer

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        try:
            model_obj = get_object_or_404(model, user=user, recipe=recipe)
            model_obj.delete()
        except MultipleObjectsReturned:
            model_obj = get_list_or_404(model, user=user, recipe=recipe)
            for obj in model_obj:
                obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        final_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__shopping_cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit__name',
            'amount'
        )
        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                final_list[name]['amount'] += item[2]
        pdfmetrics.registerFont(
            TTFont('Handicraft', 'data/Handicraft.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        page = canvas.Canvas(response)
        page.setFont('Handicraft', size=24)
        page.drawString(200, 800, 'Список покупок')
        page.setFont('Handicraft', size=16)
        height = 750
        for i, (name, data) in enumerate(final_list.items(), 1):
            page.drawString(75, height, (f'{i}. {name} - {data["amount"]} '
                                         f'{data["measurement_unit"]}'))
            height -= 25
        page.showPage()
        page.save()
        return response


class SubscriptionListView(ListAPIView):
    """Subscription model view: GET."""

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return User.objects.filter(subscribed_by__subscriber=self.request.user)


class SubscriptionViewSet(APIView):
    """Subscription model view: POST DELETE."""

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'error': 'Subscription to oneself not allowed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscription.objects.filter(
                subscriber=request.user,
                author_id=user_id
        ).exists():
            return Response(
                {'error': 'You are already subscribed to this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = get_object_or_404(User, id=user_id)
        Subscription.objects.create(
            subscriber=request.user,
            author_id=user_id
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        get_object_or_404(User, id=user_id)
        subscription = Subscription.objects.filter(
            subscriber=request.user,
            author_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'You are not subscribed to this user.'},
            status=status.HTTP_400_BAD_REQUEST
        )
