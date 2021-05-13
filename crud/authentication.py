from rest_framework.authentication import TokenAuthentication

from .models import AuthToken


class AuthTokenAuthentication(TokenAuthentication):
    model = AuthToken
