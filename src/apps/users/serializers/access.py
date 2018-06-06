from rest_framework import serializers

from apps.users.models import StaffAccess


class StaffAccessSerializer(serializers.ModelSerializer):
    """
    Staff access (permission)
    """
    name = serializers.CharField(source='access.name')
    logo = serializers.ImageField(source='access.logo', read_only=True)

    class Meta:
        model = StaffAccess
        fields = ('id', 'name', 'logo', 'active')
        extra_kwargs = {
            'id': {
                'required': True,
                'read_only': False
            }
        }
