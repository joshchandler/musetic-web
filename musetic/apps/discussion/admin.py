from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Discussion, DiscussionVote, DiscussionFlag


class DiscussionAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Content'),
         {'fields': ('user', 'submission', 'comment')}),
        (_('Metadata'),
         {'fields': ('date_submitted', 'is_deleted')}),
    )

    list_display = ('user', 'date_submitted', 'is_deleted')
    list_filter = ('date_submitted', 'is_deleted')
    date_hierarchy = 'date_submitted'
    ordering = ('-date_submitted',)
    raw_id_fields = ('user', 'submission',)
    search_fields = ('user', 'submission',)


class DiscussionVoteAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Content'),
         {'fields': ('vote_type', 'discussion', 'voter',)}),
    )


class DiscussionFlagAdmin(admin.ModelAdmin):
    fieldset = (
        (_('Content'),
         {'fields': ('user', 'discussion', 'flag',)}),
        (_('Metadata'),
         {'fields': ('date_flagged',)})
    )


admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(DiscussionVote, DiscussionVoteAdmin)
admin.site.register(DiscussionFlag, DiscussionFlagAdmin)
