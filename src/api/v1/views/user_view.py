from ..serializers.user_serializer import (
    UserSerializer,
    LoginUserSerializer,
    ForgetPasswordSerializer,
    ResetPasswordSerializer,
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
from rest_framework.views import APIView
from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from ..paginations.user_pagination import UserPagination


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
    permission_classes = [AllowAny]

    def create(self, request):
        """
        This method is used to generate the new access and refresh token if access token is expired.
        """
        if 'refresh' not in request.data:
            return Response({'error': 'Refresh token is not found.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            refresh_token = RefreshToken(request.data['refresh'])
            user_id = refresh_token['user_id']
            user = User.objects.get(id=user_id)
            refresh_token.blacklist()
            token = get_tokens_for_user(user)
            return Response(
                {
                'access': f'{token['access']}',
                'refresh': f'{token['refresh']}',
                },
                status=status.HTTP_200_OK
            )
        except TokenError:
            return Response({'error': 'Token already expired, Login again.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)


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


class ForgetPasswordView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(**serializer.validated_data)
            except User.DoesNotExist:
                return Response({'error': f'User with these {serializer.validated_data['email']} email not found.'},
                    status=status.HTTP_404_NOT_FOUND)

            encode_user_id = urlsafe_base64_encode(force_bytes(user.id))
            encode_user_token = PasswordResetTokenGenerator().make_token(user)
            link = f'http://localhost:3000/reset-password/{encode_user_id}/{encode_user_token}'

            subject = 'Reset Password.'
            message = f'Hello Sir/Mam\nFor Reset your password click: {link}'
            from_email = settings.EMAIL_HOST_USER
            to_email = [user.email]
            send_mail(subject, message, from_email, to_email)
            return Response({'success': 'Reset password email sent to your email.'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        encode_user_id = kwargs.get('encode_user_id')
        encode_user_token = kwargs.get('encode_user_token')
        user_id = int(smart_str(urlsafe_base64_decode(encode_user_id)))
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User is not found.'}, status=status.HTTP_404_NOT_FOUND)
        if not PasswordResetTokenGenerator().check_token(user, encode_user_token):
            return Response({'error': 'Password token is not valid.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['password'] != serializer.validated_data['confirm_password']:
                return Response({'error': 'Password not match with confirm password.'},
                                status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['confirm_password'])
            user.save()
            return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': f'User created successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
