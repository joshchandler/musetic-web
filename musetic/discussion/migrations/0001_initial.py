# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('comment', models.TextField(verbose_name='comment', max_length=3000)),
                ('date_submitted', models.DateTimeField(verbose_name='date/time submitted', default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(verbose_name='date/time updated', null=True, auto_now=True)),
                ('is_deleted', models.BooleanField(verbose_name='is deleted', help_text='Check this box to delete the comment', default=False)),
                ('submission', models.ForeignKey(verbose_name='submission', to='submission.Submission', related_name='submission_discussions')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL, related_name='user_discussions')),
            ],
            options={
                'verbose_name': 'Discussion',
                'verbose_name_plural': 'Discussions',
            },
        ),
        migrations.CreateModel(
            name='DiscussionFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('reason', models.CharField(verbose_name='reason', db_index=True, max_length=300)),
                ('date_flagged', models.DateTimeField(verbose_name='date', default=django.utils.timezone.now)),
                ('discussion', models.ForeignKey(verbose_name='discussion', to='discussion.Discussion', related_name='flags')),
                ('flagger', models.ForeignKey(verbose_name='flagger', to=settings.AUTH_USER_MODEL, related_name='discussion_flags')),
            ],
            options={
                'verbose_name': 'discussion flag',
                'verbose_name_plural': 'discussion flags',
                'db_table': 'discussion_flag',
            },
        ),
        migrations.CreateModel(
            name='DiscussionVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('vote_type', models.BooleanField(default=True)),
                ('discussion', models.ForeignKey(to='discussion.Discussion', related_name='discussion_votes')),
                ('voter', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_discussion_votes')),
            ],
            options={
                'db_table': 'discussion_vote',
            },
        ),
        migrations.AlterUniqueTogether(
            name='discussionvote',
            unique_together=set([('discussion', 'voter')]),
        ),
        migrations.AlterUniqueTogether(
            name='discussionflag',
            unique_together=set([('flagger', 'discussion')]),
        ),
    ]
