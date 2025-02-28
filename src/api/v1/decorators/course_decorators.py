from user.models import User
from rest_framework.response import Response
from rest_framework import status

def resolve_assignee_name(view_method):
    """
    Decorator used to take the full_name as input or designation of the user,
    Based on the input we are search the user in the database.
    :param view_method: method.
    :return: function.
    """
    def wrapper(self, request, *args, **kwargs):
        if 'full_name' in request.data:
            full_name = request.data['full_name'].strip()
            first_name, last_name = full_name.split()
            try:
                user = User.objects.get(first_name=first_name, last_name=last_name)
                request.data.pop('full_name')
            except User.DoesNotExist:
                return Response({'error': 'User with these name is not exists.'}, status=status.HTTP_404_NOT_FOUND)
            except User.MultipleObjectsReturned:
                return Response({'error': 'User with these name is more than one.'}, status=status.HTTP_404_NOT_FOUND)
        elif 'designation' in request.data:
            user = User.objects.filter(designation__choice_name=request.data['designation']).first()
            if not user:
                return Response({'error': 'User with these designation is not exists.'}, status=status.HTTP_404_NOT_FOUND)
            request.data.pop('designation')
        else:
            return Response({'error': 'Full Name or designation are not provided.'}, status=status.HTTP_404_NOT_FOUND)

        request.data['user'] = user.id
        return view_method(self, request, *args, **kwargs)

    return wrapper
