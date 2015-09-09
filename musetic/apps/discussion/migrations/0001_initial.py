# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('submission', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('comment', models.TextField(max_length=3000, verbose_name='comment')),
                ('date_submitted', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date/time submitted')),
                ('date_updated', models.DateTimeField(null=True, auto_now=True, verbose_name='date/time updated')),
                ('is_deleted', models.BooleanField(help_text='Check this box to delete the comment', verbose_name='is deleted', default=False)),
                ('submission', models.ForeignKey(related_name='submission_discussions', to='submission.Submission', verbose_name='submission')),
                ('user', models.ForeignKey(related_name='user_discussions', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Discussion',
                'verbose_name_plural': 'Discussions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiscussionFlag',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('reason', models.CharField(max_length=300, verbose_name='reason', db_index=True)),
                ('date_flagged', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date')),
                ('discussion', models.ForeignKey(related_name='flags', to='discussion.Discussion', verbose_name='discussion')),
                ('flagger', models.ForeignKey(related_name='discussion_flags', to=settings.AUTH_USER_MODEL, verbose_name='flagger')),
            ],
            options={
                'verbose_name_plural': 'discussion flags',
                'verbose_name': 'discussion flag',
                'db_table': 'discussion_flag',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiscussionVote',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('vote_type', models.BooleanField(default=True)),
                ('discussion', models.ForeignKey(related_name='discussion_votes', to='discussion.Discussion')),
                ('voter', models.ForeignKey(related_name='user_discussion_votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'discussion_vote',
            },
            bases=(models.Model,),
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
