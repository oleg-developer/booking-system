from rest_framework import serializers

from apps.common.models import Country
from apps.users.models import User, Chief
from apps.auth_core.models import AuthToken


class SignUpSerializer(serializers.ModelSerializer):
    """
    Registration
    """
    country = serializers.PrimaryKeyRelatedField(write_only=True,
                                                 queryset=Country.objects.all())
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'country')

    def create(self, validated_data):
        country = validated_data.pop('country')

        validated_data['username'] = validated_data['email']
        user = super(SignUpSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        # создаем объект владельца (Chief) и связываем с пользователем (User)
        Chief.objects.create(user=user, country=country)

        return user


class AuthTokenSerializer(serializers.ModelSerializer):
    """
    Authorization Token
    """
    def to_representation(self, instance):
        return {'token': instance.key}

    class Meta:
        model = AuthToken
        fields = ('key', 'client', 'version', 'platform')


class RecoverPasswordSerializer(serializers.Serializer):
    """
    Password recovery
    """
    email = serializers.EmailField()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Change Password
    """
    old_pass = serializers.CharField(required=True)
    new_pass = serializers.CharField(required=True)


class SignInSerializer(serializers.Serializer):
    """
    Authorization
    """
    username = serializers.CharField()
    password = serializers.CharField(min_length=6)
