from django.db.models.functions import TruncMonth
from rest_framework import mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.auth_core.authentication import TokenAuthentication
from apps.auth_core.permissions import TokenRequired, IsAuthenticated
from apps.hotels.permissions import HotelRequired
from apps.hotels.serializers import DistanceTypeSerializer, \
    LocationTypeSerializer, StreetTypeSerializer, HotelListSerializer, \
    HotelEquipmentSections, HotelEqItemUpdateSerializer, GuestListSerializer, \
    GuestSerializer, GuestCreateUpdateSerializer, BookingCalendarSerializer
from apps.hotels.models import DistanceType, LocationType, StreetType, \
    Hotel, EquipmentSection, HotelEquipmentItem, Guest, Order, HotelRoom


class HotelViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin,
                   GenericViewSet):
    """
    API for working with information related to hotels (Hotel)
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenRequired, IsAuthenticated, HotelRequired)

    @list_route(methods=['get'])
    def distance(self, request):
        """
        Getting a list of "distance types"
        :param request: 
        :return: 
        """
        queryset = DistanceType.objects.all()
        serializer = DistanceTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def streets(self, request):
        """
        Getting a list of "street types"
        :param request: 
        :return: 
        """
        queryset = StreetType.objects.all()
        serializer = StreetTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def location(self, request):
        """
        Getting a list of "locations"
        :param request: 
        :return: 
        """
        queryset = LocationType.objects.all()
        serializer = LocationTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        """
        Receive information related only to the current user's hotel
        :return: 
        """
        hotel = self.request.user.get_hotel()
        queryset = Hotel.objects.filter(id=hotel.id)
        return queryset

    def get_serializer_class(self):
        """
        Getting the right class of the serializer, depending on the method
        :return:
        """
        serializer_dict = {
            'list': HotelListSerializer,
            'update': HotelListSerializer
        }
        if self.action in serializer_dict.keys():
            return serializer_dict[self.action]
        else:
            return HotelListSerializer


class HotelEquipmentViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin,
                            GenericViewSet):
    """
    API for working with hotel facilities (HotelEquipment)
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenRequired, IsAuthenticated, HotelRequired)
    serializer_class = HotelEqItemUpdateSerializer

    def get_queryset(self):
        """
        Receive information related only to the current user's hotel
        :return: 
        """
        hotel = self.request.user.get_hotel()
        queryset = HotelEquipmentItem.objects.filter(hotel_id=hotel.id)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Getting a list of the equipment of the hotel, grouped by type
        :return:
        """
        hotel = request.user.get_hotel()
        sections = EquipmentSection.objects.all()
        serializer = HotelEquipmentSections(sections, many=True,
                                            context={'hotel_id': hotel.id})
        return Response(serializer.data)


class GuestsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin, mixins.UpdateModelMixin,
                    GenericViewSet):
    """
    API for working with information about guests (Guest)
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenRequired, IsAuthenticated, HotelRequired)

    def list(self, request, *args, **kwargs):
        """
        List of hotel guests, grouped by the month of arrival
        :return: 
        """
        hotel = request.user.get_hotel()

        months = Order.objects \
            .filter(room__hotel=hotel) \
            .annotate(date=TruncMonth('arrival_date')) \
            .values('date') \
            .distinct()

        serializer = GuestListSerializer(months, many=True,
                                         context={'hotel_id': hotel.id})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Creating a guest object (Guest)
        :return: 
        """
        hotel = request.user.get_hotel()
        # It is necessary to clearly indicate the hotel for which a guest is being created
        request.data.update({'hotel': hotel.id})

        serializer = GuestCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        detail_serializer = GuestSerializer(instance=instance)
        return Response(detail_serializer.data)

    def get_queryset(self):
        """
        Receive information related only to the current user's hotel
        :return: 
        """
        hotel = self.request.user.get_hotel()
        return Guest.objects.filter(hotel_id=hotel.id)

    def get_serializer_class(self):
        """
        Getting the right class of the serializer, depending on the method
        :return:
        """
        serializer_dict = {
            'retrieve': GuestSerializer,
            'update': GuestCreateUpdateSerializer
        }
        if self.action in serializer_dict.keys():
            return serializer_dict[self.action]
        else:
            return None


class BookingViewset(mixins.ListModelMixin, GenericViewSet):
    """
    API for working with booking information
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (TokenRequired, IsAuthenticated, HotelRequired)

    def get_queryset(self):
        hotel = self.request.user.get_hotel()
        return HotelRoom.objects.filter(hotel=hotel)

    def list(self, request, *args, **kwargs):
        search_values = None  # search options
        from_date = request.GET.get('from', None),
        to_date = request.GET.get('to', None),
        capacity = request.GET.get('capacity', None)

        if from_date and to_date and capacity:
            search_values = {
                'from_date': from_date,
                'to_date': to_date,
                'capacity': capacity
            }

        hotel = request.user.get_hotel()
        buildings = HotelRoom.objects.filter(hotel=hotel) \
            .values('building') \
            .distinct()

        serializer = BookingCalendarSerializer(
            buildings, many=True, context={
                'hotel_id': hotel.id, 'search_values': search_values
            }
        )
        return Response(serializer.data)
