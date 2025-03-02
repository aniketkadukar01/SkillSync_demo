from ..serializers.user_serializer import (
    UserSerializer,
    LoginUserSerializer,
    ForgetPasswordSerializer,
    ResetPasswordSerializer,
)
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
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from ..paginations.user_pagination import UserPagination
from ..tasks.send_email_for_reset_password import send_forgot_password_email


def get_tokens_for_user(user):
    """
    This method is used to create new access and refresh token.
    :param user: instance of current user.
    :return: access and refresh token.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(ViewSet):
    """This View is used for user Login"""

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
    """This View is used for create refresh token"""

    permission_classes = [AllowAny]

    def create(self, request):
        """
        This method is used to generate the new access and refresh token if access token is expired.
        """
        if 'refresh' not in request.data:
            return Response({'error': 'Refresh token is not found.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            refresh_token = RefreshToken(request.data['refresh'])
            user_id = refresh_token.payload['user_id']
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
        except KeyError:  # Catch key error if user_id is not in the payload.
            return Response({'error': 'Invalid refresh token payload.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(ViewSet):
    """This View is used for user Logout."""

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
    """This View is used for user Logout from all sessions."""

    def create(self, request):
        """
        This method is used to log out user from all the devices.
        """
        # If user is authenticated then authentication middleware set the current user.
        # Delete all the OutstandingToken and Blacklisted data from the database,
        # So user can't create new access token from the old refresh token.
        OutstandingToken.objects.filter(user=request.user).delete()
        return Response({'success': 'Logout from all devices successfully.'}, status=status.HTTP_200_OK)


class ForgetPasswordView(APIView):
    """This View is used for user forgot password."""

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        This method create encode user_id and user_token based on email passed and sent back a link through email.
        This link is for frontend on click that link a new page open for reset password.
        :param request: email
        :param args: position arguments if any
        :param kwargs: keywords arguments if any.
        :return: email to user.
        """
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

            send_forgot_password_email.apply_async(args=[user.email, link])
            return Response({'success': 'Reset password email sent to your email.'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """This View is used for user reset-password password."""

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        This method used of that encode user_id and user_token for user Recognition which passed in forgot password api.
        After user is known then password is validated and update in database
        :param request: password and confirm password which user want to update.
        :param args: position arguments if any.
        :param kwargs: encode user_id and user_token.
        :return: success message.
        """
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
    """This View is used for user operation api."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination

    def create(self, request, *args, **kwargs):
        """
        This method is used to create and return success message to user.
        :param request: user data.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: success message.
        """
        super().create(request, *args, **kwargs)
        return Response({'success': f'User created successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
        This method is used to destroy and return success message to user.
        :param request: none.
        :param args: position arguments if any.
        :param kwargs: user id.
        :return: success message.
        """
        super().destroy(request, *args, **kwargs)
        return Response({'success': f'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class MeApiView(APIView):
    """This View is used for retrieve user."""

    def get(self, request, *args, **kwargs):
        """
        This method is used to retrieve the user data based on the user_id passed in jwt token.
        :param request: none.
        :param args: position arguments if any.
        :param kwargs: keywords arguments if any.
        :return: user data.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
