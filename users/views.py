# users/views.py
from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserSerializer,
    LoginOrRegisterUserSerializer
)
from .utils import get_jwt_token_from_user


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = [
        "first_name",
        "last_name",
        "is_active",
        "username",
        "email",
    ]
    ordering_fields = [
        "first_name",
        "last_name",
        "username",
        "email",
    ]

    # ordering = ["-created_at"]

    def get_queryset(self):
        request = self.request
        queryset = self.queryset
        return queryset

    def get_serializer_class(self):
        return UserSerializer

    @action(detail=False)
    def me(self, request):
        """
        User can get their own data.

        Response:
            - HTTP 200 OK
            - User data
        """
        serializer = self.get_serializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class LoginOrRegisterViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = LoginOrRegisterUserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        register_flag = data.pop('register_flag')
        if register_flag is False:
            try:
                user = get_user_model().objects.get(email=email)
                if user.check_password(password):
                    serializer = LoginOrRegisterUserSerializer(user)
                    message = "User Longed In"
                    status_a = status.HTTP_200_OK
                else:
                    return Response({"error": "Wrong Password"}, status=status.HTTP_404_NOT_FOUND)
            except ObjectDoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = LoginOrRegisterUserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            message = "User Registered"
            status_a = status.HTTP_201_CREATED
            user = get_user_model().objects.get(email=serializer.data.get('email'))
        access_token, refresh_token = get_jwt_token_from_user(user=user)
        user_data = serializer.data
        response_data = {
            "email": user_data.get('email'),
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": message,
        }
        return Response(
            response_data,
            status=status_a,
        )