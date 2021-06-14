from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegistrationAPIView.as_view(), name='user_registration'),
    path('posts/<str:pk>/like/', views.LikeAPIView.as_view(), name='like'),
    path('analytics/', views.get_analytics, name='analytics')
]
