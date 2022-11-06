from djoser import utils
from djoser.conf import settings
from djoser.views import TokenCreateView
from recipes.models import Tag
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import TagSerializer


class CustomTokenCreateView(TokenCreateView):
    '''Custom Token create view.

    Override response status code from 200_OK to 201_CREATED'''

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
    pagination_class = None
