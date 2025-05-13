from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .models import User

def get_jwt_token_from_user(user):
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    return str(access_token), str(refresh_token)


def get_user_from_jwt_token(token_str):
    try:
        jwt_authentication = JWTAuthentication()
        validated_token = jwt_authentication.get_validated_token(token_str)
        user = jwt_authentication.get_user(validated_token)
        return user

    except AuthenticationFailed as e:
        print(f"Authentication failed: {str(e)}")
        return None

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None


def validate_unique_user_email(email, user=None):
    all_users = User.objects.all_with_deleted()
    if user:
        return not all_users.exclude(pk=user.pk).filter(email=email).exists()
    return not all_users.filter(email=email).exists()
