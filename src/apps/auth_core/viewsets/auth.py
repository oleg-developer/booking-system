from django.contrib.auth import authenticate, logout
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.auth_core.authentication import TokenAuthentication
from apps.auth_core.models import AuthToken
from apps.auth_core.permissions import TokenRequired, IsAuthenticated
from apps.auth_core.serializers import ChangePasswordSerializer
from apps.auth_core.serializers import SignInSerializer, SignUpSerializer, \
    AuthTokenSerializer, RecoverPasswordSerializer
from apps.auth_core.utils import send_confirmation_email, \
    recover_password
from apps.users.models import User

from apps.users.serializers import UserShortSerializer, UserEmailSerializer


class AuthViewSet(GenericViewSet):
    """
    ViewSet for implementing methods related to authorization
    """
    serializer_class = AuthTokenSerializer
    authentication_classes = (TokenAuthentication,)

    permission_classes = (TokenRequired, IsAuthenticated)

    @list_route(methods=['post'], permission_classes=())
    def handshake(self, request):
        """
        Obtaining an authorization token / user information
        :param request: 
        :return: 
        """
        token_string = 'Token {}'

        if isinstance(request.auth, AuthToken):
            """
            If there is a token and the user is authorized, then return
            information about the user
            """

            if request.user.is_authenticated():
                user_serializer = UserShortSerializer(instance=request.user)
                return Response(user_serializer.data)
            else:
                """
                If the token exists, but the user is not authorized,
                deny access
                """
                return Response(data={'detail': _('User not authorized')},
                                status=status.HTTP_401_UNAUTHORIZED)

        """
        Creating a new token
        """
        serializer = AuthTokenSerializer(data=request.data,
                                         instance=request.auth)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={},
            status=status.HTTP_200_OK,
            headers={
                'Authorization': token_string.format(serializer.data['token'])
            }
        )

    @list_route(methods=['post'], permission_classes=(TokenRequired,))
    def signin(self, request):
        """
        Authorization
        :param request: 
        :return: 
        """
        user = request.user
        if not request.user.is_authenticated():
            serializer = SignInSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user is None:
                return Response(
                    {'detail': _('Wrong username/password')},
                    status=status.HTTP_400_BAD_REQUEST
                )

        request.auth.user = user
        request.auth.save()

        serializer = UserShortSerializer(instance=user)

        return Response(serializer.data)

    @list_route(methods=['get'])
    def signout(self, request):
        """
        Logout
        :param request: 
        :return: 
        """
        request.auth.user = None
        request.auth.save()
        logout(request)
        return Response({'detail': _("You successfully logout")})

    @list_route(methods=['post'], permission_classes=(TokenRequired,))
    def signup(self, request):
        """
        Registration
        :param request: 
        :return: 
        """
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_confirmation_email(request, user)
        email_serializer = UserEmailSerializer(instance=user)
        return Response(email_serializer.data)

    def get_serializer_class(self):
        """
        Getting the right class of the serializer, depending on the method
        :return: 
        """
        serializer_dict = {
            'handshake': AuthTokenSerializer,
            'signin': SignInSerializer,
            'signup': SignUpSerializer,
            'change_password': ChangePasswordSerializer
        }
        if self.action in serializer_dict.keys():
            return serializer_dict[self.action]
        else:
            return AuthTokenSerializer

    @list_route(methods=['post'], permission_classes=(TokenRequired,))
    def recover_password(self, request):
        """
        Password recovery
        :param request:
        :return:
        """
        serializer = RecoverPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).last()
        if user is None:
            return Response(data={'detail': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)
        recover_password(request, user)
        return Response(data={'detail': 'OK'},
                        status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def change_password(self, request):
        """
        Change password
        :return: 
        """
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get('old_pass')):
                return Response({'old_pass': ['Wrong password.']},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get('new_pass'))
            user.save()
            return Response({'detail': 'success'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
