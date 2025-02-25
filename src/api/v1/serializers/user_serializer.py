from rest_framework import serializers
# noinspection PyUnresolvedReferences
from user.models import User
from utils.models import Choice
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields['email'].required = False
            self.fields['password'].required = False

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
        fields = ['email', 'password', 'first_name', 'last_name', 'username', 'status', 'type',]
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    type = serializers.StringRelatedField(allow_null = True, required=False,)
    status = serializers.StringRelatedField(allow_null=True, required=False,)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    class Meta:
        model = User
        fields = ['first_name', 'last_name' ,'email', 'type', 'username', 'status']


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label='Email address',
        max_length=254,
        write_only=True,
    )
    password = serializers.CharField(max_length=128, write_only=True)
