from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class CustomUser(AbstractBaseUser):
    identifier = models.CharField(max_length=40, unique=True)

    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = ['identifier']
