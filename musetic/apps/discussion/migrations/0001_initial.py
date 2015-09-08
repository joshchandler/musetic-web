# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('comment', models.TextField(max_length=3000, verbose_name='comment')),
                ('date_submitted', models.DateTimeField(verbose_name='date/time submitted', default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date/time updated', null=True)),
                ('is_deleted', models.BooleanField(help_text='Check this box to delete the comment', verbose_name='is deleted', default=False)),
                ('submission', models.ForeignKey(to='submission.Submission', verbose_name='submission', related_name='submission_discussions')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='user', related_name='user_discussions')),
            ],
            options={
                'verbose_name': 'Discussion',
                'verbose_name_plural': 'Discussions',
            },
        ),
        migrations.CreateModel(
            name='DiscussionFlag',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('reason', models.CharField(max_length=300, verbose_name='reason', db_index=True)),
                ('date_flagged', models.DateTimeField(verbose_name='date', default=django.utils.timezone.now)),
                ('discussion', models.ForeignKey(to='discussion.Discussion', verbose_name='discussion', related_name='flags')),
                ('flagger', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='flagger', related_name='discussion_flags')),
            ],
            options={
                'verbose_name': 'discussion flag',
                'db_table': 'discussion_flag',
                'verbose_name_plural': 'discussion flags',
            },
        ),
        migrations.CreateModel(
            name='DiscussionVote',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('vote_type', models.BooleanField(default=True)),
                ('discussion', models.ForeignKey(related_name='discussion_votes', to='discussion.Discussion')),
                ('voter', models.ForeignKey(related_name='user_discussion_votes', to=settings.AUTH_USER_MODEL)),
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
