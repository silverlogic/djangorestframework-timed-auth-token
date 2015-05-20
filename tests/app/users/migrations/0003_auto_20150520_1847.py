# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('users', '0002_customuser_is_active'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', users.models.CustomUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(related_name='user_set', verbose_name='groups', blank=True, to='auth.Group', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(related_name='user_set', verbose_name='user permissions', blank=True, to='auth.Permission', related_query_name='user', help_text='Specific permissions for this user.'),
        ),
    ]
