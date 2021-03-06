import json

import pytest

from django.core.urlresolvers import reverse

from rest_framework import status

from timed_auth_token.models import TimedAuthToken

from users.models import CustomUser


pytestmark = pytest.mark.django_db


@pytest.fixture
def data():
    user = CustomUser(identifier='test')
    user.set_password('test')
    user.save()
    return {'username': 'test', 'password': 'test'}


def test_can_login_with_correct_info(data, client):
    # Make sure you can login multiple times
    for _ in range(3):
        response = client.post(reverse('auth:login'), data)
        assert response.status_code == status.HTTP_201_CREATED


def test_login_successful_response_data(data, client):
    content = json.loads(client.post(reverse('auth:login'), data).content.decode('utf-8'))
    token = TimedAuthToken.objects.all()[0]
    assert 'token' in content
    assert token.key in content['token']


def test_cant_login_with_non_existant_username(data, client):
    data['username'] = 'nobody'
    response = client.post(reverse('auth:login'), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'That identifier does not exist.' in response.content.decode('utf-8')


def test_cant_login_with_wrong_password(data, client):
    data['password'] = 'wrong'
    response = client.post(reverse('auth:login'), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Incorrect password.' in response.content.decode('utf-8')


def test_cant_login_if_user_is_inactive(client):
    user = CustomUser(identifier='inactive_user', is_active=False)
    user.set_password('test')
    user.save()

    response = client.post(reverse('auth:login'), {'username': 'inactive_user', 'password': 'test'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert 'inactive or deleted' in response.content.decode('utf-8')
