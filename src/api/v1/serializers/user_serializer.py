from rest_framework import serializers
# noinspection PyUnresolvedReferences
from user.models import User
from utils.models import Choice
from django.contrib.auth.hashers import make_password
import re

class UserSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError('Email is not in proper format.')
        return value

    def validate_phone_number(self, value):
        pattern = r'^\d{10}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError('Number must be 10 digit and no letter is allowed.')
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['status'] = str(instance.status.choice_name) if data['status'] else data['status']
        data['type'] = str(instance.type.choice_name) if data['type'] else data['type']
        return data

    def create(self, validated_data):
        """
        :param validated_data: Date which is required while creating the user.
        :return: Created user.
        """
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        :param instance: User instance which we want to update.
        :param validated_data: Date which is required while updating the user.
        :return: Update User instance.
        """
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'username', 'status', 'type', 'phone_number',]
        extra_kwargs = {
            'password': {'write_only': True},
        }


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label='Email address',
        max_length=254,
        write_only=True,
    )
    password = serializers.CharField(max_length=128, write_only=True)
