from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField(label='Username', validators=[RegexValidator('^[\w.@+-]+$')], max_length=150, min_length=1)
    first_name = serializers.CharField(label='First name', max_length=30)
    last_name = serializers.CharField(label='Last name', max_length=150)
    is_active = serializers.BooleanField(label='Active', default=True)


class UserWriteOnlySerializer(UserBaseSerializer):
    password = serializers.CharField(
        label='Password', validators=[RegexValidator('^(?=.*[A-Z])(?=.*\d).{8,}$')], max_length=128, min_length=1, write_only=True
    )

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class UserReadOnlySerializer(UserBaseSerializer):

    id = serializers.IntegerField(label='Id', read_only=True)
    last_login = serializers.DateTimeField(label='Last login', read_only=True)
    is_superuser = serializers.BooleanField(label='Superuser status', read_only=True)
