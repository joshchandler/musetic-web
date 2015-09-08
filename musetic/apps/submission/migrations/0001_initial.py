# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields
import django.core.files.storage
import django.utils.timezone
import musetic.apps.submission.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('reason', models.CharField(max_length=300, verbose_name='Reason')),
                ('flagger', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_flags')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, blank=True, editable=False)),
                ('submission_type', models.CharField(max_length=255, choices=[('art', 'art'), ('design', 'design'), ('imagery', 'imagery'), ('sound', 'sound'), ('video', 'video'), ('writing', 'writing')], verbose_name='Submission Type')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('url', models.URLField(unique=True, verbose_name='Link')),
                ('description', models.TextField(verbose_name='Description')),
                ('flagged', models.BooleanField(default=False, verbose_name='Is Flagged for Review')),
                ('score', models.FloatField(default=0.0)),
                ('thumbnail', models.ImageField(max_length=6144, upload_to=musetic.apps.submission.models.thumbnail_file_path, blank=True, storage=django.core.files.storage.FileSystemStorage())),
                ('date_submitted', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(null=True, auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_submissions')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('vote_type', models.BooleanField(default=True)),
                ('submission', models.ForeignKey(to='submission.Submission', related_name='submission_votes')),
                ('voter', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_votes')),
            ],
        ),
        migrations.AddField(
            model_name='flag',
            name='submission',
            field=models.ForeignKey(to='submission.Submission', related_name='submission_flags'),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('submission', 'voter')]),
        ),
    ]
