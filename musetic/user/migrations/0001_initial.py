# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('url', models.URLField(unique=True, verbose_name='Link to your Work')),
                ('is_creator', models.BooleanField(default=False, verbose_name='is creator')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='creator')),
            ],
            options={
                'db_table': 'user_usercreator',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('first_name', models.CharField(null=True, blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(null=True, blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(verbose_name='email address', max_length=254, null=True)),
                ('subject', models.CharField(max_length=300)),
                ('body', models.TextField(max_length=2000)),
            ],
            options={
                'verbose_name_plural': 'feedback',
                'verbose_name': 'feedback',
                'db_table': 'user_userfeedback',
            },
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('activation_key', models.CharField(verbose_name='activation key', max_length=40)),
                ('invitee', models.EmailField(unique=True, verbose_name='invitee email address', max_length=254)),
                ('date_invited', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date invited')),
                ('accepted', models.BooleanField(default=False, verbose_name='accepted')),
                ('inviter', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_inviter')),
            ],
            options={
                'db_table': 'user_userinvite',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('description', models.TextField(null=True, blank=True, verbose_name='Write something about yourself!')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile')),
            ],
            options={
                'db_table': 'user_userprofile',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('show_feedback_tab', models.BooleanField(default=True)),
                ('mail_comment_notifications', models.BooleanField(default=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='user_settings')),
            ],
            options={
                'db_table': 'user_usersettings',
            },
        ),
        migrations.AlterUniqueTogether(
            name='invite',
            unique_together=set([('inviter', 'invitee')]),
        ),
    ]
