=====
About
=====
A new authentication backend for Django REST framework that uses a token with
an expiration date.  A new token is created every time a user logs in.  The
token expiration date is refreshed every time the token is used.  It supports
custom user models

How To Use
==========
Add to your installed apps

.. code:: python

    INSTALLED_APPS = (
        ...
        'timed_auth_token',
    )

Add the authentication class to the default authentication classes

.. code:: python

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'timed_auth_token.authentication.TimedAuthTokenAuthentication',
        )
    }

The app comes with a login URL at /login.  The endpoint expects two parameters:
username and password.

.. code:: python

    url_patterns = [
        ...
        # Can login by using /auth/login
        url(r'^auth/', include('timed_auth_token.urls', namespace='auth')),
    ]

After a successful login the response contains one key: `token`.

.. code::

    {'token': 'lkjalsdjf8asdkjfal;kdfa8s;dlna;sdf'}

To use this token to authenticate it must be included in the HTTP headers:

.. code::

    Authorization: Token YOURTOKEN


Configuration
=============
The only available configuration option is the duration of the token.  It
defaults to 30 days.  You can set it either on the user model as an attribute
or as a setting in your settings.py.  If they are both set, the user model will
take precedence.

#. Put it on your user model as an attribute

   .. code:: python

        from datetime import timedelta
        from django.contrib.auth.models import User

        class MyUserModel(User):
            token_validity_duration = timedelta(days=60)

#. Put it in your settings.py

   .. code:: python

        from datetime import timedelta

        TIMED_AUTH_TOKEN = {
            'DEFAULT_VALIDITY_DURATION': timedelta(days=45)
        }


Credits
=======
Starting code (model, auth backend) thanks to Jake from `jh.gg <https://jh.gg/>`_.
