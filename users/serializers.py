from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'balance']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.updated_by = self.context["request"].user
        instance.save()
        return instance


class LoginOrRegisterUserSerializer(serializers.ModelSerializer):
    register_flag = serializers.BooleanField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'register_flag']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
