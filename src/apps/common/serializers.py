from rest_framework import serializers

from apps.common.models import Phone
from apps.common.models import Country


class CountrySerializer(serializers.ModelSerializer):
    """
    Country
    """
    class Meta:
        model = Country
        fields = ('id', 'code', 'name', 'logo')


class PhoneSerializer(serializers.ModelSerializer):
    """
    Phone
    """
    class Meta:
        model = Phone
        fields = ('id', 'main', 'option')
        extra_kwargs = {
            'id': {
                'required': True,
                'read_only': False
            }
        }
