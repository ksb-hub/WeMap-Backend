from django.urls import path, include

from .views import RegisterAPIView, AuthAPIView, UserUpdateView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name='register'),
    path("auth/", AuthAPIView.as_view(), name='auth'),
    path("auth/update/", UserUpdateView.as_view(), name='user_update'),
    path("auth/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
]