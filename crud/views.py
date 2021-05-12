from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserWriteOnlySerializer, UserReadOnlySerializer
from django.contrib.auth.models import User


class UserView(APIView):
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
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
        return Response({"success": "User '{}' created successfully".format(user_saved.username)})

    def put(self, request, pk):
        saved_user = get_object_or_404(User.objects.all(), pk=pk)
        data = request.data
        serializer = UserWriteOnlySerializer(instance=saved_user, data=data)

        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()

        return Response({"success": "User '{}' updated successfully".format(user_saved.username)})

    def delete(self, request, pk):
        user = get_object_or_404(User.objects.all(), pk=pk)
        user.delete()
        return Response({"message": "User with id `{}` has been deleted.".format(pk)}, status=204)

    def patch(self, request, pk):
        saved_user = get_object_or_404(User.objects.all(), pk=pk)
        data = request.data
        serializer = UserWriteOnlySerializer(instance=saved_user, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()

        return Response({"success": "User '{}' updated successfully".format(user_saved.username)})
