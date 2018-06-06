from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.users.models import User


@api_view(['GET'])
def email_confirm(request, user_id, token):
    """
    Sending a confirmation email
    :param request: Http request 
    :param user_id: User id
    :param token: Token value
    :return: 
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # TODO: return page with error
        return None

    expected_token = user.get_registration_token()

    if expected_token == token:
        user.is_active = True
        user.save()
    else:
        # TODO: return page with error
        pass

    # TODO: return page (redirect) "mail successfully confirmed"
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def recover_password(request, user_id, token):
    """
    Sending a confirmation email
    :param request: Http request
    :param user_id: User id
    :param token: Token value
    :return:
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # TODO: return page with error
        return None

    expected_token = user.get_recover_token()

    if expected_token != token:
        # TODO: return page with error
        pass

    # TODO: return page (redirect) "mail successfully confirmed"
    return Response(status=status.HTTP_200_OK)
