import os
import base64

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from .settings import token_settings


class TimedAuthTokenManager(models.Manager):
    def filter_for_user(self, user):
        '''A queryset with all of the auth tokens for the `user`.'''
        queryset = self.get_queryset()
        return queryset.filter(object_id=user.id, content_type=ContentType.objects.get_for_model(user))


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
    objects = TimedAuthTokenManager()
    key = models.CharField(max_length=40, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField(blank=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    user = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return u'%s.%s:%i, created %s, expires %s' % (
            self.content_type.app_label, self.content_type.name, self.object_id, self.created, self.expires
        )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()

        if not self.expires:
            self.calculate_new_expiration()

        super(TimedAuthToken, self).save(*args, **kwargs)

    def calculate_new_expiration(self):
        validity_duration = getattr(self.content_type.model_class(), 'token_validity_duration',
                                    token_settings.DEFAULT_VALIDITY_DURATION)
        self.expires = timezone.now() + validity_duration

    @property
    def is_expired(self):
        return self.expires < timezone.now()

    @staticmethod
    def generate_key():
        return base64.urlsafe_b64encode(os.urandom(30)).decode()
