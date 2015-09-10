# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invite',
            options={},
        ),
        migrations.AlterField(
            model_name='invite',
            name='invitee',
            field=models.EmailField(max_length=75, verbose_name='invitee email address', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invite',
            name='inviter',
            field=models.ForeignKey(related_name='user_inviter', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='invite',
            unique_together=set([('inviter', 'invitee')]),
        ),
    ]
