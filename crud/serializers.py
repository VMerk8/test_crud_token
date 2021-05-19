from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class UserReadOnlySerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'is_active', 'id', 'last_login', 'is_superuser']


class UserWriteOnlySerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'is_active']
        extra_kwargs = {'first_name': {'required': True},
                        'last_name': {'required': True},
                        'is_active': {'required': True},
                        'username': {'validators': [RegexValidator('^[\w.@+-]+$')]},
                        'password': {'validators': [RegexValidator('^(?=.*[A-Z])(?=.*\d).{8,}$')]}}


    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        password = validated_data.get('password')
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        password = validated_data.get('password', instance.password)
        instance.set_password(password)
        instance.save()
        return instance


class TokenSerializer(serializers.Serializer):

    username = serializers.CharField(label='Username', min_length=1)
    password = serializers.CharField(label='Password', min_length=1)
