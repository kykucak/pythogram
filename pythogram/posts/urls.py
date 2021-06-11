from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<str:pk>/like', views.like_post, name='like_post'),
    path('posts/<str:pk>/unlike', views.unlike_post, name='unlike_post')
]
