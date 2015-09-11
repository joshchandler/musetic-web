# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import musetic.avatar.models
from django.conf import settings
import s3_folder_storage.s3
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('primary', models.BooleanField(default=False)),
                ('avatar', models.ImageField(storage=s3_folder_storage.s3.DefaultStorage(), blank=True, upload_to=musetic.avatar.models.avatar_file_path, max_length=6144)),
                ('date_uploaded', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
