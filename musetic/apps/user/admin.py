from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, Creator, Invite, Feedback


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = True
    verbose_name_plural = 'users'


class UsersAdmin(UserAdmin):
        inlines = (ProfileInline,)


class CreatorInline(admin.ModelAdmin):
    model = Creator
    can_delete = True
    verbose_name = 'creator'
    verbose_name_plural = 'creators'


class InviteInline(admin.ModelAdmin):
    model = Invite
    can_delete = True
    verbose_name = 'invite'
    verbose_name_plural = 'invites'


class FeedbackInline(admin.ModelAdmin):
    model = Feedback
    list_display = ['first_name', 'last_name', 'email', 'subject', 'body']
    can_delete = True
    verbose_name = 'feedback'
    verbose_name_plural = 'feedback'


admin.site.unregister(User)
admin.site.register(User, UsersAdmin)
admin.site.register(Creator, CreatorInline)
admin.site.register(Invite, InviteInline)
admin.site.register(Feedback, FeedbackInline)
