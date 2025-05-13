# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    LoginOrRegisterViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='normal-user-api')
router.register(r'login-or-register', LoginOrRegisterViewSet, basename='user-login-register-api')

urlpatterns = [
    path('', include(router.urls)),
]
