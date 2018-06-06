from datetime import datetime

from django.db.models import Q
from rest_framework import serializers

from apps.common.models import Country
from apps.hotels.models import DistanceType, StreetType, LocationType, \
    HotelEquipmentItem, Hotel, Address, EquipmentSection, Guest, HotelRoom
from apps.hotels.models.order import Order
from apps.hotels.models import RoomType


class DistanceTypeSerializer(serializers.ModelSerializer):
    """
    Type of distance
    """

    class Meta:
        model = DistanceType
        fields = ('id', 'label', 'value')


class StreetTypeSerializer(serializers.ModelSerializer):
    """
    Street type
    """

    class Meta:
        model = StreetType
        fields = ('id', 'label', 'value')


class LocationTypeSerializer(serializers.ModelSerializer):
    """
    Location type
    """

    class Meta:
        model = LocationType
        fields = ('id', 'label', 'value')


class HotelEquipmentSections(serializers.ModelSerializer):
    """
    Category of the hotel's equipment
    """
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        hotel_id = self.context.get('hotel_id', None)
        queryset = HotelEquipmentItem.objects.filter(hotel_id=hotel_id,
                                                     equipment_item__section_id=obj.id)
        serializer = HotelEquipmentItemSerializer(instance=queryset, many=True)
        return serializer.data

    class Meta:
        model = EquipmentSection
        fields = ('title', 'label', 'items')


class HotelNameSerializer(serializers.ModelSerializer):
    """
    The name of the hotel
    """

    class Meta:
        model = Hotel
        fields = ('id', 'name')


class HotelEquipmentItemSerializer(serializers.ModelSerializer):
    """
    Elements of hotel equipment
    """
    label = serializers.CharField(source='equipment_item.label')

    class Meta:
        model = HotelEquipmentItem
        fields = ('id', 'label', 'active')


class AddressSerializer(serializers.ModelSerializer):
    """
    Address
    """
    country = serializers.CharField(source='hotel.chief.country')
    street_type = serializers.PrimaryKeyRelatedField(
        queryset=StreetType.objects.all())
    distance_type = serializers.PrimaryKeyRelatedField(
        queryset=DistanceType.objects.all())
    location_type = serializers.PrimaryKeyRelatedField(
        queryset=LocationType.objects.all())

    def get_street_type(self, obj):
        return obj.street_type.id if obj.street_type else None

    def get_distance_type(self, obj):
        return obj.distance_type.id if obj.distance_type else None

    class Meta:
        model = Address
        fields = (
            'street', 'distance', 'country', 'street_type', 'location_type',
            'house', 'building', 'distance_type', 'latitude', 'longitude')

    def to_representation(self, instance):
        ret = super(AddressSerializer, self).to_representation(instance)
        ret['coordinates'] = {
            'lat': ret.pop('latitude', None),
            'lng': ret.pop('longitude', None)
        }
        return ret


class HotelListSerializer(serializers.ModelSerializer):
    """
    Hotels list
    """
    hotel_id = serializers.IntegerField(source='id')
    address = AddressSerializer()
    registration_time = serializers.JSONField(write_only=True)

    class Meta:
        model = Hotel
        fields = ('hotel_id', 'name', 'address', 'phone', 'email', 'website',
                  'description', 'rating', 'rating_confirmed',
                  'registration_from', 'registration_to',
                  # write only fields:
                  'registration_time')

    def update(self, instance, validated_data):

        # update of an attached Address object
        address_data = validated_data.pop('address', None)
        hotel_data = address_data.pop('hotel', None)
        try:
            country_str = hotel_data['chief']['country']
        except KeyError:
            country_str = None

        if country_str and country_str != instance.chief.country.name:
            country_obj = Country.objects.filter(
                name__iexact=country_str).last()
            if not country_obj:
                country_obj = Country.objects.create(name=country_str)

            instance.chief.country = country_obj
            instance.chief.save()

        address_obj, created = Address.objects.update_or_create(
            id=instance.address_id,
            defaults=address_data)

        if created:
            instance.address = address_obj
            instance.save()

        # unpacking fields registration_from, registration_to for later saving
        registration_time = validated_data.pop('registration_time', None)
        if registration_time:
            validated_data['registration_from'] = registration_time.get('from',
                                                                        None)
            validated_data['registration_to'] = registration_time.get('to',
                                                                      None)

        return super(HotelListSerializer, self).update(instance,
                                                       validated_data)

    def to_representation(self, instance):
        ret = super(HotelListSerializer, self).to_representation(instance)
        ret['registration_time'] = {
            'from': ret.pop('registration_from', None),
            'to': ret.pop('registration_to', None)
        }
        return ret


class HotelEqItemUpdateSerializer(serializers.ModelSerializer):
    """
    Renovation of the equipment element of the hotel
    """

    class Meta:
        model = HotelEquipmentItem
        fields = ('id', 'active')


class RoomHotelSerializer(serializers.ModelSerializer):
    """
    Room of the hotel
    """

    class Meta:
        model = HotelRoom
        fields = ('number', 'price', 'title')


class RoomTypeSeriializer(serializers.ModelSerializer):
    """
    Type of room
    """

    class Meta:
        model = RoomType
        fields = ('type', 'name')


class OrderSerializer(serializers.ModelSerializer):
    """
    Order/booking
    """
    total_price = serializers.FloatField(source='get_total_price')
    room_id = serializers.IntegerField(source='room.number')
    room_title = serializers.CharField(source='room.title')
    room_price = serializers.FloatField(source='room.price')

    class Meta:
        model = Order
        fields = (
            'room_id', 'room_price', 'room_title', 'arrival_date',
            'leave_date',
            'total_price', 'payment_status')


class GuestSerializer(serializers.ModelSerializer):
    """
    Guest
    """
    orders = OrderSerializer(many=True)

    class Meta:
        model = Guest
        fields = (
            'id', 'first_name', 'second_name', 'last_name', 'email', 'agent',
            'information', 'orders')  # 'phone')


class GuestCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Create / update guest information
    """
    hotel = serializers.PrimaryKeyRelatedField(
        write_only=True,
        required=True,
        queryset=Hotel.objects.all()
    )

    class Meta:
        model = Guest
        fields = (
            'hotel', 'first_name', 'second_name', 'last_name', 'email',
            'agent', 'information')  # phone)


class GuestShortSerializer(serializers.ModelSerializer):
    """
    Guest: full name
    """

    class Meta:
        model = Guest
        fields = ('id', 'full_name')


class GuestListSerializer(serializers.Serializer):
    """
    Serializing the list of guests grouped by the arrival month (arrival date)
    """
    date = serializers.DateTimeField()
    guests = serializers.SerializerMethodField()

    def get_guests(self, obj):
        """
        Receiving a guest list for each month
         (month of check in the hotel is taken into account)
        :param obj: a serializable object of the form {'date': datetime} 
        :return:
        """
        try:
            month = obj['date'].month
        except:
            return []

        hotel_id = self.context.get('hotel_id', None)
        queryset = Guest.objects.filter(
            orders__isnull=False,
            orders__arrival_date__month=month,
            orders__room__hotel_id=hotel_id
        ).distinct()

        serializer = GuestShortSerializer(instance=queryset, many=True)
        return serializer.data

    class Meta:
        fields = ('date', 'guests')


class TimeLineSerializer(serializers.ModelSerializer):
    """
    Period of reservation
    """
    begin = serializers.DateTimeField(source='arrival_date')
    end = serializers.DateTimeField(source='leave_date')
    type = serializers.CharField(source='payment_status')

    class Meta:
        model = Order
        fields = ('begin', 'end', 'type')


class RoomSerializer(serializers.ModelSerializer):
    """
    Hotel Room
    """
    timeline = serializers.SerializerMethodField()

    class Meta:
        model = HotelRoom
        fields = (
            'id', 'number', 'title', 'photo', 'number_group', 'double_bed',
            'single_bed', 'bunk_bed', 'timeline')

    def get_timeline(self, obj):
        """
        Receiving the booking period
        """
        orders = obj.orders.all()
        search_values = self.context.get('search_values', None)

        if search_values is None:
            serializer = TimeLineSerializer(instance=orders, many=True)
            return serializer.data

        # If the number capacity is less than the required one, then return an empty list
        if obj.capacity < int(search_values.get('capacity', 0)):
            return []

        # TODO: define date format in settings
        from_date = datetime.strptime(search_values['from_date'], '%d.%m.%y')
        to_date = datetime.strptime(search_values['to_date'], '%d.%m.%y')

        """If there is an order within the required date
         (that is, the number on these days is busy or booked), return an empty list
        """
        q = ~(Q(arrival_date__gt=to_date) | Q(leave_date__lt=from_date))
        if orders.filter(q).exists():
            return []

        serializer = TimeLineSerializer(instance=orders, many=True)
        return serializer.data


class FloorSerializer(serializers.Serializer):
    """
    Floor
    """
    floor = serializers.IntegerField()
    rooms = serializers.SerializerMethodField()

    def get_rooms(self, obj):
        """
        Getting list of rooms on the floor
        """
        search_values = self.context.get('search_values', None)
        hotel_id = self.context.get('hotel_id', None)
        building = self.context.get('building', None)
        floor = obj.get('floor', None)

        rooms = HotelRoom.objects.filter(hotel_id=hotel_id, building=building,
                                         floor=floor)
        serializer = RoomSerializer(rooms, many=True, context={
            'search_values': search_values
        })
        return serializer.data

    class Meta:
        fields = ('floor','rooms')


class BookingCalendarSerializer(serializers.Serializer):
    """
    Booking calendar
    """
    building = serializers.CharField()
    floors = serializers.SerializerMethodField()

    def get_floors(self, obj):
        search_values = self.context.get('search_values', None)
        hotel_id = self.context.get('hotel_id', None)
        building = obj['building']
        floors = HotelRoom.objects \
            .filter(hotel__id=hotel_id, building=building) \
            .values('floor') \
            .distinct()

        floor_serializer = FloorSerializer(
            floors, many=True,
            context={
                'hotel_id': hotel_id,
                'building': building,
                'search_values': search_values
            })
        return floor_serializer.data

    class Meta:
        fields = ('building','floors')
