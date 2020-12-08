from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    CommentViewSet,
    TitleViewSet,
    get_confirmation_code,
    get_token,
    profile
)

api_v1_router = DefaultRouter()
api_v1_router.register('users', UserViewSet, basename='users')
api_v1_router.register('categories', CategoryViewSet, basename='categories')
api_v1_router.register('genres', GenreViewSet, basename='genres')
api_v1_router.register('titles', TitleViewSet, basename='titles')
api_v1_router.register(
    r'titles/(?P<title_id>.+)/reviews', ReviewViewSet, 'reviews'
)
api_v1_router.register(
    r'titles/(?P<title_id>.+)/reviews/(?P<review_id>.+)/comments',
    CommentViewSet, 'comments'
)

urlpatterns = [
    path('v1/users/me/', profile, name='profile'),
    path('v1/', include(api_v1_router.urls)),
    path('auth/email/', get_confirmation_code,
         name='get_confirmation_code'),
    path('auth/token/', get_token, name='get_token'),
]
