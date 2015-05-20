import json

import pytest

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rest_framework import status

from timed_auth_token.models import TimedAuthToken

from users.models import CustomUser


pytestmark = pytest.mark.django_db


# User model path, User model, Username field
@pytest.fixture(params=[('auth.User', User, 'username'),
                        ('users.CustomUser', CustomUser, 'identifier')])
def data(request, settings):
    settings.AUTH_USER_MODEL = request.param[0]
    user = request.param[1](**{request.param[2]: 'test'})
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
    assert 'That username does not exist.' in response.content.decode('utf-8')


def test_cant_login_with_wrong_password(data, client):
    data['password'] = 'wrong'
    response = client.post(reverse('auth:login'), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Incorrect password.' in response.content.decode('utf-8')
