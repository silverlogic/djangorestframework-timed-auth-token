from datetime import timedelta

from django.conf import settings


DEFAULT = {
    'DEFAULT_VALIDITY_DURATION': timedelta(days=30)
}


class TokenSettings:
    def __getattr__(self, key):
        try:
            return settings.TIMED_AUTH_TOKEN[key]
        except AttributeError:
            return DEFAULT[key]

    def __getitem__(self, key):
        return self.__getattr__(key)


token_settings = TokenSettings()
