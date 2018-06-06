import os
import binascii

from django.urls import reverse

from apps.auth_core.tasks import send_email


def generate_string(length=20):
    """
    Generating an authorization token
    :param length: key length
    :return: string
    """
    return binascii.hexlify(os.urandom(length)).decode()


def send_confirmation_email(request, user, token=None):
    """
    Sending a letter with a link to confirm registration
    :param request: Http Request
    :param user: User object
    :param token: str the value of the token used for activation
    :return:
    """

    token = token or user.get_registration_token()

    # registration confirmation link
    url_path = reverse('dashboard:email_confirm', kwargs={
        'user': user.id,
        'token': token
    })

    context = {
        'url': request.build_absolute_uri(url_path),
        'url_path': url_path,
        'user': {
            'full_name': user.get_full_name()
        }
    }

    send_email.delay("Confirm email", 'email_confirm', context, [user.email])


def recover_password(request, user, token=None):
    """
    Sending an email with a link for password recovery
    :param request: Http Request
    :param user: User object
    :param token: str the value of the token used to recover the password
    :return:
    """

    token = token or user.get_recovery_token()

    # password recovery link
    url_path = reverse('dashboard:recover_password', kwargs={
        'user': user.id,
        'token': token
    })

    context = {
        'url': request.build_absolute_uri(url_path),
        'url_path': url_path,
        'user': {
            'full_name': user.get_full_name()
        }
    }

    send_email.delay("Recover password", 'recover_password', context,
                     [user.email])
