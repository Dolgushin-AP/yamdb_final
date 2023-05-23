from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import user_register, get_jwt_token
from .views import (CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet,
                    CommentViewSet,
                    ReviewViewSet)

from users.views import UsersViewSet

router_v1 = SimpleRouter()

router_v1.register(
    'users',
    UsersViewSet,
    basename='users'
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)

router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', user_register, name='user_register'),
    path('v1/auth/token/', get_jwt_token, name='get_jwt_token'),
]
