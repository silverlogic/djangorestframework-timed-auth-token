from datetime import timedelta

import pytest

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone

from rest_framework import status

from timed_auth_token.models import TimedAuthToken


pytestmark = pytest.mark.django_db


@pytest.fixture
def token():
    user = User.objects.create(username='test', password='test', email='test@tset.com')
    return TimedAuthToken.objects.create(user=user)


def test_can_access_with_token(client, token):
    response = client.get(reverse('test_authentication'), HTTP_AUTHORIZATION='Token {}'.format(token.key))
    assert response.status_code == status.HTTP_200_OK


def test_cant_access_without_header(client):
    response = client.get(reverse('test_authentication'))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_cant_access_with_invalid_token(client):
    response = client.get(reverse('test_authentication'), HTTP_AUTHORIZATION='Token blkjasdfk')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'Invalid token' in response.content.decode('utf-8')


def test_cant_access_without_token(client):
    response = client.get(reverse('test_authentication'), HTTP_AUTHORIZATION='Token')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_cant_access_with_expired_token(client, token):
    token.expires = timezone.now() - timedelta(days=1)
    token.save()
    response = client.get(reverse('test_authentication'), HTTP_AUTHORIZATION='Token {}'.format(token.key))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'Token has expired' in response.content.decode('utf-8')


def test_cant_access_with_token_that_belongs_to_inactive_user(client, token):
    token.user.is_active = False
    token.user.save()
    response = client.get(reverse('test_authentication'), HTTP_AUTHORIZATION='Token {}'.format(token.key))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'User inactive or deleted' in response.content.decode('utf-8')
