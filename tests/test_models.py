from datetime import timedelta

import pytest

from django.utils import timezone

from timed_auth_token.models import TimedAuthToken

from users.models import CustomUser


pytestmark = pytest.mark.django_db


@pytest.fixture
def token():
    return TimedAuthToken(user=CustomUser.objects.create(identifier='blah'))


def test_calculate_new_expiration_uses_30_day_default(token):
    token.calculate_new_expiration()
    expected = timezone.now().date() + timedelta(days=30)
    actual = token.expires.date()
    assert expected == actual


def test_calculate_new_expiration_duration_can_be_set_in_settings(token, settings):
    settings.TIMED_AUTH_TOKEN = {'DEFAULT_VALIDITY_DURATION': timedelta(days=5)}
    token.calculate_new_expiration()
    expected = timezone.now().date() + timedelta(days=5)
    actual = token.expires.date()
    assert expected == actual


def test_calculate_new_expiration_can_be_overridden_on_model(token, settings):
    settings.TIMED_AUTH_TOKEN = {'DEFAULT_VALIDITY_DURATION': timedelta(days=5)}
    CustomUser.token_validity_duration = timedelta(days=10)
    token.calculate_new_expiration()
    expected = timezone.now().date() + timedelta(days=10)
    actual = token.expires.date()
    assert expected == actual
