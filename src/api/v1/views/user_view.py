from ..serializers.user_serializer import (
    UserSerializer,
    UserProfileSerializer,
    LoginUserSerializer,
)
# noinspection PyUnresolvedReferences
from user.models import User
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet, ModelViewSet
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.exceptions import TokenError


def get_tokens_for_user(user):
    """
    :param user: instance of current user.
    :return: access and refresh token.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        """
        This method is used to authenticate and create the token for user.
        """
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, **serializer.validated_data)
            if not user:
                return Response({'error': 'user not found.'}, status=status.HTTP_404_NOT_FOUND)
            token = get_tokens_for_user(user)
            return Response(
                {
                    'access': f'{token['access']}',
                    'refresh': f'{token['refresh']}',
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateRefreshTokenView(ViewSet):
    def create(self, request):
        """
        This method is used to generate the new access and refresh token if access token is expired.
        """
        if 'refresh' not in request.data:
            return Response({'error': 'Refresh token is not found.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            token = get_tokens_for_user(request.user)
            return Response(
                {
                'access': f'{token['access']}',
                'refresh': f'{token['refresh']}',
                },
                status=status.HTTP_200_OK
            )
        except TokenError:
            return Response({'error': 'Token already expired, Login again.'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(ViewSet):
    def create(self, request):
        """
        This method is used to log out the user.
        """
        if 'refresh' not in request.data:
            return Response({'error': 'Refresh token is not found.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            return Response({'success': 'logout successfully.'}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'error':'Token is already expired, Login again.'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(ViewSet):
    def create(self, request):
        """
        This method is used to log out user from all the devices.
        """
        # If user is authenticated then authentication middleware set the current user.
        # Delete all the OutstandingToken and Blacklisted data from the database
        # So user can't create new access token from the old refresh token.
        OutstandingToken.objects.filter(user=request.user).delete()
        return Response({'success': 'Logout from all devices successfully.'}, status=status.HTTP_200_OK)


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': f'User created successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer
        return super().get_serializer_class()
