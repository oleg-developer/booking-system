from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.auth_core.authentication import TokenAuthentication
from apps.auth_core.permissions import TokenRequired
from apps.common.models import Country
from apps.common.serializers import CountrySerializer


class CountryViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    Viewset for working with countries (getting a list of countries)
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenRequired,)
