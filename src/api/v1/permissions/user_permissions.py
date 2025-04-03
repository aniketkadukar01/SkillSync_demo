from rest_framework import permissions
# from django_otp.plugins.otp_totp.models import TOTPDevice

# class Is2FAEnabled(permissions.BasePermission):
#     def has_permission(self, request, view):
#         user = request.user
#
#         if not user.is_authenticated():
#             return False
#
#         device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
#         return device is not None
#