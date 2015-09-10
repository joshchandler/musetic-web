# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import django.utils.timezone
import musetic.apps.avatar.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('primary', models.BooleanField(default=False)),
                ('avatar', models.ImageField(max_length=6144, upload_to=musetic.apps.avatar.models.avatar_file_path, storage=django.core.files.storage.FileSystemStorage(), blank=True)),
                ('date_uploaded', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
