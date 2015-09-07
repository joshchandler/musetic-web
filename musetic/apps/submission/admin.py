from django.contrib.admin import ModelAdmin, site

from . import models


class SubmissionAdmin(ModelAdmin):
    list_display = ['submission_type', 'title', 'score', 'flagged', 'user', 'date_submitted']
    list_filter = ['submission_type', 'flagged', 'score']
    search_fields = ['title', 'description', 'user', 'date_submitted']


class VoteAdmin(ModelAdmin):
    list_display = ['vote_type', 'submission', 'voter']
    search_fields = ['submission', 'voter']


class FlagAdmin(ModelAdmin):
    list_display = ['reason', 'submission', 'flagger']
    search_fields = ['submission', 'flagger']


site.register(models.Submission, SubmissionAdmin)
site.register(models.Vote, VoteAdmin)
site.register(models.Flag, FlagAdmin)
