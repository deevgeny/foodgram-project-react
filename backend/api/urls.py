from django.urls import include, path, re_path
from djoser import views as djoser_views
from rest_framework.routers import DefaultRouter

from . import views as api_views

app_name = 'api'
router = DefaultRouter()

router.register('tags', api_views.TagViewSet)
router.register('ingredients', api_views.IngredientViewSet)
router.register('recipes', api_views.RecipeViewSet)

urlpatterns = [
    re_path(r"^auth/token/login/?$",
            api_views.CustomTokenCreateView.as_view(), name="login"),
    re_path(r"^auth/token/logout/?$",
            djoser_views.TokenDestroyView.as_view(), name="logout"),
    path('users/subscriptions/',
         api_views.SubscriptionListView.as_view(), name='subscriptions'),
    path('users/<int:user_id>/subscribe/',
         api_views.SubscriptionViewSet.as_view(), name='subscribe'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
]
