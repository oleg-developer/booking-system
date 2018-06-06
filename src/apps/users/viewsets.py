from rest_framework.viewsets import ModelViewSet

from apps.auth_core.authentication import TokenAuthentication
from apps.auth_core.permissions import TokenRequired, IsAuthenticated

from apps.users.models import Staff
from apps.users.permission import StaffPermission
from apps.users.serializers.staff import StaffListSerializer, \
    StaffDetailSerializer


class StaffViewSet(ModelViewSet):
    """
    API for working with staff objects (Staff)
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenRequired, IsAuthenticated,
                          StaffPermission)

    def get_queryset(self):
        """
        Select only employees available to the current user
        :return: 
        """
        queryset = Staff.objects.filter(chief=self.request.user.chief)
        return queryset

    def get_serializer_class(self):
        """
        Getting the right class of the serializer, depending on the method
        :return:
        """
        serializer_dict = {
            'list': StaffListSerializer,
            'retrieve': StaffDetailSerializer,
            'update': StaffDetailSerializer
        }
        if self.action in serializer_dict.keys():
            return serializer_dict[self.action]
        else:
            return StaffDetailSerializer
