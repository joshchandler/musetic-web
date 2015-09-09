from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile, Creator, Invite, Feedback


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = True
    verbose_name_plural = 'users'


class UsersAdmin(UserAdmin):
    inlines = (ProfileInline,)


class CreatorInline(admin.ModelAdmin):
    model = Creator
    list_display = ['user', 'url', 'is_creator']
    can_delete = True
    verbose_name = 'creator'
    verbose_name_plural = 'creators'


class InviteInline(admin.ModelAdmin):
    list_display = ['inviter', 'invitee', 'accepted', 'date_invited']
    list_filter = ['inviter', 'accepted']
    can_delete = True
    verbose_name = 'invite'
    verbose_name_plural = 'invites'


class FeedbackInline(admin.ModelAdmin):
    model = Feedback
    list_display = ['email', 'subject', 'body']
    can_delete = True
    verbose_name = 'feedback'
    verbose_name_plural = 'feedback'


admin.site.unregister(User)
admin.site.register(User, UsersAdmin)
admin.site.register(Creator, CreatorInline)
admin.site.register(Invite, InviteInline)
admin.site.register(Feedback, FeedbackInline)
