from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import AuthToken
from .serializers import (TokenSerializer, UserReadOnlySerializer,
                          UserWriteOnlySerializer)


class UserView(ModelViewSet):

    permission_classes = [IsAuthenticated]

    serializer_class = UserWriteOnlySerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return UserReadOnlySerializer
        if self.action == 'retrieve':
            return UserReadOnlySerializer
        return self.serializer_class

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class TokenView(APIView):

    def post(self, request):
        authorization_data = request.data
        serializer = TokenSerializer(data=authorization_data)
        key = None
        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.validated_data
            saved_user = get_object_or_404(
                User.objects.all(), username=valid_data['username'], is_active=True
            )
            password_is_valid = saved_user.check_password(raw_password=valid_data['password'])
            if password_is_valid:
                key = AuthToken.objects.get(user=saved_user).key
        return Response({"token": key})
