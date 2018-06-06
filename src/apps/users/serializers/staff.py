from rest_framework import serializers

from apps.common.models import Phone
from apps.common.serializers import PhoneSerializer
from apps.common.utils import update_nested_phones
from apps.users.models import Staff, StaffAccess
from apps.users.serializers.access import StaffAccessSerializer


class StaffListSerializer(serializers.ModelSerializer):
    """
    Staff list
    """
    name = serializers.CharField(source='full_name')

    class Meta:
        model = Staff
        fields = ('id', 'name', 'photo', 'position')


class StaffDetailSerializer(serializers.ModelSerializer):
    """
    Staff details
    """
    email = serializers.EmailField(source='user.email', allow_null=True)
    login = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password', write_only='')
    accesses = StaffAccessSerializer(many=True)
    phones = PhoneSerializer(many=True)

    class Meta:
        model = Staff
        fields = (
            "id", "photo", 'full_name', 'first_name', 'second_name', 'last_name',
            'email', 'position', 'phones', 'login', 'password', 'is_locked',
            'accesses')

    def update(self, instance, validated_data):
        # update nested User object
        user_data = validated_data.pop('user', None)
        updating_fields = ['username', 'email', 'password']
        update_nested_user(user_data, instance.user, updating_fields)

        # update nested StaffAccess object
        staff_accesses = validated_data.pop('accesses', None)
        update_nested_accesses(staff_accesses)

        # update nested Phone object
        phones = validated_data.pop('phones', None)
        update_nested_phones(phones, instance, Phone)

        return super(StaffDetailSerializer, self).update(instance,
                                                         validated_data)


def update_nested_accesses(data):
    """
    Update nested objects
    :param data: updating data
    :return: 
    """
    # It is assumed that all access datacomes to the server,
    # and not only those that have active = True

    while data:
        access = data.pop(0)
        # remove nested object 'Access'
        access.pop('access', None)
        try:
            inst = StaffAccess.objects.get(id=access.get('id'))
        except StaffAccess.DoesNotExist:
            continue
        inst.active = access.get('active', inst.active)
        inst.save()


def update_nested_user(data, user, updating_fields):
    """
    Update nested User object
    :param data: updating data
    :param user: updating User object
    :param updating_fields: updating fields list
    :return: 
    """

    for field in updating_fields:
        setattr(user, field, data.get(field, user.username))

    if 'password' in updating_fields:
        new_password = data.get('password', user.password)
        password_is_valid = new_password == user.password or \
                            user.check_password(new_password)

        if not password_is_valid:
            user.set_password(new_password)

    user.save()
