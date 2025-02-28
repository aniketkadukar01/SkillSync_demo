from rest_framework import serializers
from user.models import User
from utils.models import Choice
from django.contrib.auth.hashers import make_password
import re


class UserSerializer(serializers.ModelSerializer):
    """This Serializer is used for user operation"""

    def validate_email(self, value):
        """
        This method id used to validate the user email based on the pattern provided.
        :param value: user email.
        :return: validated email.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError('Email is not in proper format.')
        return value

    def validate_phone_number(self, value):
        """
        This method is used to validate the user phone_number based on the pattern provided.
        :param value: user phone_number.
        :return: validate phone_number.
        """
        pattern = r'^\d{10}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError('Number must be 10 digit and no letter is allowed.')
        return value

    def to_representation(self, instance):
        """
        This method executes during the serialization process of data.
        If we want to change the data of instance or want to make any changes before the response sent.
        :param instance: current instance which passed to become serialized.
        :return: serialized data.
        """
        data = super().to_representation(instance)

        data['status'] = str(instance.status.choice_name) if data['status'] else data['status']
        data['type'] = str(instance.type.choice_name) if data['type'] else data['type']
        return data

    def create(self, validated_data):
        """
        This method called the create_user method to create the user and make the password hash,
        so that we don't have to handle password hashing explicitly.
        :param validated_data: Date which is required while creating the user.
        :return: Created user.
        """
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        This method is handle the password hashing of the user while update the user data,
        if the user want to update the password.
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
        fields = ['email', 'password', 'first_name', 'last_name', 'username', 'status', 'type', 'phone_number', 'designation',]
        extra_kwargs = {
            'password': {'write_only': True},
        }


class LoginUserSerializer(serializers.Serializer):
    """This Serializer is used for Login user"""

    email = serializers.EmailField(label='Email address', max_length=254, write_only=True,)
    password = serializers.CharField(max_length=128, write_only=True)


class ForgetPasswordSerializer(serializers.Serializer):
    """This Serializer is used for forgot-password of user"""

    email = serializers.EmailField(label='Email address', max_length=254,)

    def validate_email(self, value):
        """
        This method id used to validate the user email based on the pattern provided.
        :param value: user email.
        :return: validated email.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError('Email is not in proper format.')
        return value


class ResetPasswordSerializer(serializers.Serializer):
    """This Serializer is used for reset-password of user"""

    password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)
