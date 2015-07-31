from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions

from .models import TimedAuthToken


class TimedAuthTokenCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            User = get_user_model()
            self.user = User.objects.get(**{User.USERNAME_FIELD: username})
        except ObjectDoesNotExist:
            msg = _('That {} does not exist.'.format(User.USERNAME_FIELD))
            raise serializers.ValidationError(msg)

    def validate(self, data):
        password = data['password']
        if not self.user.check_password(password):
            raise serializers.ValidationError(_('Incorrect password.'))

        if not self.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return data

    def create(self, validated_data):
        return TimedAuthToken.objects.create(user=self.user)

    def to_representation(self, token):
        return TimedAuthTokenReadSerializer(token).data

    def update(self, instance, validated_data):
        raise RuntimeError('Cannot update a timed auth token.')


class TimedAuthTokenReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimedAuthToken
        fields = 'token',

    token = serializers.CharField(source='key')
