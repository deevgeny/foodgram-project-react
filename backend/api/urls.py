from django.urls import include, path, re_path
from djoser.views import TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import CustomTokenCreateView, IngredientViewSet, TagViewSet

app_name = 'api'
router = DefaultRouter()


router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include('djoser.urls')),
    # Use re_path to prevent HTTP_301_MOVED_PERMANENTLY for 'auth/token/login'
    re_path(r"^auth/token/login/?$",
            CustomTokenCreateView.as_view(), name="login"),
    re_path(r"^auth/token/logout/?$",
            TokenDestroyView.as_view(), name="logout"),
    path('', include(router.urls)),
]
