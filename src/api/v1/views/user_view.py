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
# from django_otp.plugins.otp_totp.models import TOTPDevice
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiExample, OpenApiResponse


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


@extend_schema(
    request=ForgetPasswordSerializer,
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description='Password reset email sent successfully.',
            examples=[
                OpenApiExample(
                    'Success Example',
                    description='Example of a successful response.',
                    value={"success": "Reset password email sent to your email."}
                )
            ]
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description='Bad request, validation errors occurred.',
            examples=[
                OpenApiExample(
                    'Bad Request Example',
                    description='Example of a validation error response.',
                    value={"error": "This field is required."}
                )
            ]
        ),
        404: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description='User not found with the provided email.',
            examples=[
                OpenApiExample(
                    'Not Found Example',
                    description='Example when the user is not found.',
                    value={"error": "User with this email not found."}
                )
            ]
        ),
    },
    parameters=[
        OpenApiParameter(
            name='email',
            description='The email address of the user requesting a password reset.',
            required=True,
            type=OpenApiTypes.STR,  # Corrected from OpenApiTypes.STRING to OpenApiTypes.STR
            examples=[
                OpenApiExample(
                    'Email Example',
                    description='Example of an email parameter.',
                    value='user@example.com'
                )
            ]
        )
    ],
    auth=None,  # No authentication required for this endpoint
    operation_id='requestPasswordReset',  # Custom operation ID
    examples=[
        OpenApiExample(
            'Forgot Password Request Example',
            description='Example request body for forgetting password.',
            value={"email": "user@example.com"}
        )
    ]
)
class ForgetPasswordView(APIView):
    """
    View to handle the password reset process for users who have forgotten their passwords.

    This endpoint accepts the user's email address, verifies if the user exists, and sends a password reset link
    to the provided email. The link contains an encoded user ID and token for secure password reset functionality.

    Attributes:

        authentication_classes (list): Empty list as no authentication is required to access this endpoint.
        permission_classes (list): Empty list to allow unauthenticated access.

    Methods:

        post(request, *args, **kwargs):
            Handles POST requests to initiate the password reset process.
            - Validates the provided email address.
            - Checks if the user exists in the database.
            - Generates an encoded user ID and token.
            - Sends a password reset email containing the reset link.

    Request Parameters:

        - **email** (str): The user's email address to receive the password reset link.

    Responses:

        - **200 OK**:
            {
                "success": "Reset password email sent to your email."
            }
            Indicates that the reset email was sent successfully.

        - **400 Bad Request**:
            {
                "error": "Validation error details."
            }
            Returned when the provided email is invalid or missing.

        - **404 Not Found**:
            {
                "error": "User with this email not found."
            }
            Indicates that no user exists with the provided email address.

    Example Request:

        POST /api/v1/forget-password/
        {
            "email": "user@example.com"
        }

    Example Successful Response:

        {
            "success": "Reset password email sent to your email."
        }

    Example Error Response:

        {
            "error": "User with this email not found."
        }
    """

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

    def get_permissions(self):
        """
        This method ensure that when user is created then the permission is allow any,
        otherwise the global authentication which were mentioned in the settings.
        """
        return [AllowAny()] if self.action == 'create' else super().get_permissions()

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


# class Enable2FAView(APIView):
#     """
#     This view class is used to implement 2FA.
#     first we create the url for qr code when user first request, using get handler method
#     second after scan the qrcode the otp start generating in google authenticator app, user have to enter otp to verify himself.
#     then it is successfully enable, using post handle method.
#     """
#     def get(self, request):
#         device, created = TOTPDevice.objects.get_or_create(user=request.user, confirmed=False)
#
#         if not created and device.confirmed:
#             return Response({'message': '2FA is already enabled on this device.'}, status=status.HTTP_409_CONFLICT)
#
#         return Response({'provisioning_uri': device.config_url}, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         device = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()
#
#         if device and device.verify_token(request.data.get('otp')):
#             device.confirmed = True
#             device.save()
#             return Response({'message': '2FA enabled successfully!'}, status=status.HTTP_200_OK)
#
#         return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
#
#
# class VerifyOTPView(APIView):
#     """
#     This View is used to verify otp at the time of user login.
#     View is usefull after the user successfully verified the otp firstly in the Enable2FAView.
#     """
#     def post(self, request):
#         device = TOTPDevice.objects.filter(user=request.user, confirmed=True).first()
#
#         if device and device.verify_token(request.data.get('otp')):
#             return Response({'message': 'OTP verified successfully!'}, status=status.HTTP_200_OK)
#
#         return Response({'error': 'Invalid OTP or 2FA is disabled.'}, status=status.HTTP_400_BAD_REQUEST)
#
#
# class Disable2FAView(APIView):
#     """
#     View is used to disable the 2FA.
#     """
#     def post(self, request):
#         device = TOTPDevice.objects.filter(user=request.user, confirmed=True).first()
#
#         if device and device.verify_token(request.data.get('otp')):
#             device.confirmed = False
#             device.save()
#
#             return Response({'message': '2FA has been disabled successfully.'}, status=status.HTTP_200_OK)
#
#         return Response({'error': 'No active 2FA device found.'}, status=status.HTTP_404_NOT_FOUND)
