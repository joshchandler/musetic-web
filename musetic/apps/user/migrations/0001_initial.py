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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('url', models.URLField(unique=True, verbose_name='Link to your Work')),
                ('is_creator', models.BooleanField(verbose_name='is creator', default=False)),
                ('user', models.OneToOneField(related_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_usercreator',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30, null=True)),
                ('email', models.EmailField(null=True, verbose_name='email address', max_length=75)),
                ('subject', models.CharField(max_length=300)),
                ('body', models.TextField(max_length=2000)),
            ],
            options={
                'verbose_name_plural': 'feedback',
                'verbose_name': 'feedback',
                'db_table': 'user_userfeedback',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(verbose_name='activation key', max_length=40)),
                ('invitee', models.EmailField(verbose_name='invitee email address', max_length=75)),
                ('date_invited', models.DateTimeField(verbose_name='date invited', default=django.utils.timezone.now)),
                ('accepted', models.BooleanField(verbose_name='accepted', default=False)),
                ('inviter', models.ForeignKey(related_name='inviter', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'user invites',
                'verbose_name': 'user invite',
                'db_table': 'user_userinvite',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('description', models.TextField(blank=True, verbose_name='Write something about yourself!', null=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_userprofile',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('show_feedback_tab', models.BooleanField(default=True)),
                ('mail_comment_notifications', models.BooleanField(default=True)),
                ('user', models.OneToOneField(related_name='user_settings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_usersettings',
            },
            bases=(models.Model,),
        ),
    ]
