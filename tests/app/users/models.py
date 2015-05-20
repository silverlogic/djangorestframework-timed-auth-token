from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, identifier, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not identifier:
            raise ValueError('The given username must be set')
        user = self.model(identifier=identifier,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, identifier, password=None, **extra_fields):
        return self._create_user(identifier, password, False, False, **extra_fields)

    def create_superuser(self, identifier, password, **extra_fields):
        return self._create_user(identifier, password, True, True, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    identifier = models.CharField(max_length=40, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_short_name(self):
        return self.identifier
