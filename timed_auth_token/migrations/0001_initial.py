# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TimedAuthToken',
            fields=[
                ('key', models.CharField(serialize=False, primary_key=True, max_length=40)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_used', models.DateTimeField(auto_now=True)),
                ('expires', models.DateTimeField(blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
