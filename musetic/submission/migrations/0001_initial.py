# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import musetic.submission.models
import s3_folder_storage.s3
from django.conf import settings
import uuidfield.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('reason', models.CharField(verbose_name='Reason', max_length=300)),
                ('flagger', models.ForeignKey(related_name='user_flags', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('uuid', uuidfield.fields.UUIDField(unique=True, editable=False, max_length=32, blank=True)),
                ('submission_type', models.CharField(choices=[('art', 'art'), ('design', 'design'), ('imagery', 'imagery'), ('sound', 'sound'), ('video', 'video'), ('writing', 'writing')], verbose_name='Submission Type', max_length=255)),
                ('title', models.CharField(verbose_name='Title', max_length=100)),
                ('url', models.URLField(unique=True, verbose_name='Link')),
                ('description', models.TextField(verbose_name='Description')),
                ('flagged', models.BooleanField(verbose_name='Is Flagged for Review', default=False)),
                ('score', models.FloatField(default=0.0)),
                ('thumbnail', models.ImageField(storage=s3_folder_storage.s3.DefaultStorage(), max_length=6144, blank=True, upload_to=musetic.submission.models.thumbnail_file_path)),
                ('date_submitted', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(related_name='user_submissions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('vote_type', models.BooleanField(default=True)),
                ('submission', models.ForeignKey(related_name='submission_votes', to='submission.Submission')),
                ('voter', models.ForeignKey(related_name='user_votes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='flag',
            name='submission',
            field=models.ForeignKey(related_name='submission_flags', to='submission.Submission'),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('submission', 'voter')]),
        ),
    ]
