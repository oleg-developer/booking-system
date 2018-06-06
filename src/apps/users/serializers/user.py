from rest_framework import serializers

from apps.hotels.serializers import HotelNameSerializer
from apps.users.models import User


class UserEmailSerializer(serializers.ModelSerializer):
    """
    User's email
    """
    class Meta:
        model = User
        fields = ('id', 'email')


class UserShortSerializer(serializers.ModelSerializer):
    """
    User short info
    """
    hotel = HotelNameSerializer(source='get_hotel', read_only=True)
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = User
        fields = ('id', 'email', 'hotel', 'name')
