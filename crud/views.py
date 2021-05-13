from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import AuthToken
from .serializers import (TokenSerializer, UserReadOnlySerializer,
                          UserWriteOnlySerializer)


class UserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user = User.objects.all()
        if pk:
            user = get_object_or_404(User.objects.all(), pk=pk)
            serializer = UserReadOnlySerializer(user)
            return Response({"users": serializer.data})
        else:
            serializer = UserReadOnlySerializer(user, many=True)
            return Response({"users": serializer.data})

    def post(self, request):
        user = request.data
        serializer = UserWriteOnlySerializer(data=user)
        user_saved = None
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
            AuthToken.objects.create(user=user_saved)
        return Response({"success": f"User {user_saved.username} updated successfully"})

    def put(self, request, pk):
        saved_user = get_object_or_404(User.objects.all(), pk=pk)
        data = request.data
        serializer = UserWriteOnlySerializer(instance=saved_user, data=data)
        user_saved = None

        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()

        return Response({"success": "User '{}' updated successfully".format(user_saved.username)})

    def delete(self, request, pk):
        user = get_object_or_404(User.objects.all(), pk=pk)
        user.is_active = False
        user.save()
        return Response({"success": "User '{} is not active now".format(user.username)})

    def patch(self, request, pk):
        saved_user = get_object_or_404(User.objects.all(), pk=pk)
        data = request.data
        serializer = UserWriteOnlySerializer(instance=saved_user, data=data, partial=True)

        user_saved = None
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()

        return Response({"success": "User '{}' updated successfully".format(user_saved.username)})


class TokenView(APIView):

    def post(self, request):
        authorization_data = request.data
        serializer = TokenSerializer(data=authorization_data)
        token = None
        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.validated_data
            saved_user = get_object_or_404(
                User.objects.all(), username=valid_data['username'], password=valid_data['password'],
                is_active=True
            )
            token = AuthToken.objects.get(user=saved_user)
        return Response({"token": token.key})
