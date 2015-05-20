import os
import base64

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .settings import token_settings


class TimedAuthToken(models.Model):
    '''An auth token that expires.

    The token duration is specified on the model class as a timedelta
    named `token_validity_duration`.

    If you use the included TimedAuthTokenAuthentication then the
    expiration date is refreshed every time the token is used.

    Example:
        class MyUser(models.Model):
            token_validity_duration = timedelta(days=30)

        token = TimedAuthToken(user=MyUser())

    '''
    key = models.CharField(max_length=40, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField(blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return 'Token for %s, created %s, expires %s' % (
            self.user.get_username(), self.created, self.expires
        )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()

        if not self.expires:
            self.calculate_new_expiration()

        super(TimedAuthToken, self).save(*args, **kwargs)

    def calculate_new_expiration(self):
        validity_duration = getattr(get_user_model(), 'token_validity_duration',
                                    token_settings.DEFAULT_VALIDITY_DURATION)
        self.expires = timezone.now() + validity_duration

    @property
    def is_expired(self):
        return self.expires < timezone.now()

    @staticmethod
    def generate_key():
        return base64.urlsafe_b64encode(os.urandom(30)).decode()
