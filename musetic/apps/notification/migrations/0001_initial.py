# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('level', models.CharField(default='info', choices=[('success', 'success'), ('info', 'info'), ('warning', 'warning'), ('error', 'error')], max_length=20)),
                ('unread', models.BooleanField(default=True)),
                ('actor_object_id', models.CharField(max_length=255)),
                ('verb', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('target_object_id', models.CharField(blank=True, null=True, max_length=255)),
                ('action_object_object_id', models.CharField(blank=True, null=True, max_length=255)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('public', models.BooleanField(default=True)),
                ('action_object_content_type', models.ForeignKey(blank=True, null=True, to='contenttypes.ContentType', related_name='notify_action_object')),
                ('actor_content_type', models.ForeignKey(related_name='notify_actor', to='contenttypes.ContentType')),
                ('recipient', models.ForeignKey(related_name='notifications', to=settings.AUTH_USER_MODEL)),
                ('target_content_type', models.ForeignKey(blank=True, null=True, to='contenttypes.ContentType', related_name='notify_target')),
            ],
            options={
                'ordering': ('-timestamp',),
            },
            bases=(models.Model,),
        ),
    ]
