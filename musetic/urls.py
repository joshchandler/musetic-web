from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required as auth
from django.contrib.flatpages.views import flatpage

from musetic.avatar.views import add as avatar_add, change as avatar_change, delete as avatar_delete

from musetic.discussion.views import (
    DiscussionFormView, DiscussionDelete, DiscussionVoteFormView, DiscussionFlagFormView,
    DiscussionEdit
)

# from musetic import notification
from musetic.user.views import anonymous_required
from musetic.user.views.auth import (
    RegistrationViewUniqueEmail,
    login as auth_login,
    ActivationRedirect,
    password_change,
)
from musetic.user.views.creator import (
    CreatorRequestView,
    CreatorRequestSentView,
    CreatorAcceptView,
    CreatorActivatedView
)
from musetic.user.views.feedback import (
    FeedbackView
)
from musetic.user.views.invite import (
    InviteFormView,
    AcceptInvitationView
)
from musetic.user.views.profile import (
    ProfileNewDetailView,
    ProfileTopDetailView,
)
from musetic.user.views.settings import (
    SettingsProfile,
    SettingsChangeUsername,
    SettingsChangeEmail,
    SettingsDeleteAccount,
    SettingsGeneral,
)

from musetic.submission.views import (
    SubmissionCreate, SubmissionHotList, SubmissionNewList, SubmissionTopList,
    SubmissionCategoryHotList, SubmissionCategoryNewList, SubmissionCategoryTopList, SubmissionDetail, SubmissionEdit,
    SubmissionDelete, SubmissionEditThumbnail, VoteFormView, FlagFormView
)

from musetic.submission.api import api_root, SubmissionAPIList, SubmissionAPIDetail, VoteAPIList

from rest_framework.urlpatterns import format_suffix_patterns


admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^admin/', include(admin.site.urls)),

    # API ##############################################################################################################
    url(r'^api/$', api_root),
    url(r'^api/submission/$', SubmissionAPIList.as_view(), name='submission-list'),
    url(r'^api/submission/(?P<pk>\d+)/$', SubmissionAPIDetail.as_view, name='submission-detail'),
    url(r'^api/vote/$', VoteAPIList.as_view(), name='vote-list'),

    # AUTH AND REGISTRATION ############################################################################################
    url(r'^login/$',
        anonymous_required(auth_login), name='auth_login'),
    url(r'^logout/$',
        auth_views.logout, {'template_name': 'registration/logout.html', 'next_page': '/'}, name='auth_logout'),
    url(r'^register/$',
        RegistrationViewUniqueEmail.as_view(), name='registration_register'),
    url(r'^activate/(?P<activation_key>\w+)/$',
        ActivationRedirect.as_view(), name='registration_activate',),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm, {'post_reset_redirect': 'auth_login'}, name='auth_password_reset_confirm'),

    # Add the rest of the registration app's urls
    url(r'^', include('registration.backends.default.urls')),

    # SOCIAL ###########################################################################################################
    url(r'^', include('social.apps.django_app.urls', namespace='social')),

    # USER #############################################################################################################
    url(r'^muser/(?P<username>[\w.+-]+)/$',
        ProfileNewDetailView.as_view(), name='user_profile'),
    url(r'^muser/(?P<username>[\w.+-]+)/top/$',
        ProfileTopDetailView.as_view(), name='user_profile_top'),

    # Settings
    url(r'^settings/profile/$',
        auth(SettingsProfile.as_view()), name='settings_profile'),
    url(r'^settings/username/$',
        auth(SettingsChangeUsername.as_view()), name='settings_username'),
    url(r'^settings/email/$',
        auth(SettingsChangeEmail.as_view()), name='settings_email'),
    url(r'^settings/(?P<username>[\w.+-]+)/delete/$',
        auth(SettingsDeleteAccount.as_view()), name='settings_delete'),
    url(r'^settings/password/$',
        auth(password_change), name='settings_password_change'),
    url(r'^settings/general/$',
        auth(SettingsGeneral.as_view()), name='settings_general'),

    # Invites
    url(r'^invite/$',
        auth(InviteFormView.as_view()), name='user_invite'),
    url(r'^invitation/(?P<activation_key>\w+)/$',
        AcceptInvitationView.as_view(),
        name='accept_invitation'),

    # Creator Requests
    url(r'^creator/request/$',
        auth(CreatorRequestView.as_view()), name='creator_request'),
    url(r'^creator/request/sent/$',
        auth(CreatorRequestSentView.as_view()), name='creator_request_sent'),
    url(r'^creator/(?P<username>[\w._+-]+)/accept/$',
        auth(CreatorAcceptView.as_view()), name='creator_accept'),
    url(r'^creator/(?P<username>[\w._+-]+)/accepted/$',
        auth(CreatorActivatedView.as_view()), name='creator_activated'),

    # Feedback
    url(r'^feedback/$',
        FeedbackView.as_view(), name='user_feedback'),

    # NOTIFICATION #####################################################################################################
    # url('^inbox/notifications/', include(notification.urls)),

    # AVATAR ###########################################################################################################
    url(r'^settings/avatar/$', avatar_change, name='settings_avatar'),
    url(r'^settings/avatar/add/$', avatar_add, name='settings_avatar_add'),
    url(r'^settings/avatar/delete/$', avatar_delete, name='settings_avatar_delete'),
    url(r'^avatar/', include('musetic.avatar.urls')),

    # DISCUSSION #######################################################################################################
    url(r'^(?P<slug>[\w-]+)/(?P<uuid>[^/]+)/discussion/$', DiscussionFormView.as_view(), name='discussion_form'),
    url(r'^(?P<slug>[\w-]+)/(?P<uuid>[^/]+)/discussion/(?P<pk>\d+)/flag/$',
        auth(DiscussionFlagFormView.as_view()), name='discussion_flag'),
    url(r'^(?P<slug>[\w-]+)/(?P<uuid>[^/]+)/discussion/(?P<pk>\d+)/edit/$',
        auth(DiscussionEdit.as_view()), name='discussion_edit'),
    url(r'^(?P<slug>[\w-]+)/(?P<uuid>[^/]+)/discussion/(?P<pk>\d+)/delete/$',
        auth(DiscussionDelete.as_view()), name='discussion_delete'),
    url(r'^vote/discussion/$', auth(DiscussionVoteFormView.as_view()), name='discussion_vote'),

    # SUBMISSION #######################################################################################################
    url(r'^vote/$', auth(VoteFormView.as_view()), name='vote'),
    url(r'^$', SubmissionHotList.as_view(), name='index'),
    url(r'^new/$', SubmissionNewList.as_view(), name='index_new'),
    url(r'^top/$', SubmissionTopList.as_view(), name='index_top'),
    url(r'^submit/$', auth(SubmissionCreate.as_view()), name='submit'),
    url(r'^(?P<slug>[\w-]+)/$', SubmissionCategoryHotList.as_view(), name='category'),
    url(r'^(?P<slug>[\w-]+)/new/$', SubmissionCategoryNewList.as_view(), name='category_new'),
    url(r'^(?P<slug>[\w-]+)/top/$', SubmissionCategoryTopList.as_view(), name='category_top'),
    url(r'^(?P<slug>[\w-]+)/(?P<uuid>[^/]+)/$', SubmissionDetail.as_view(), name='submission_detail'),
    url(r'^(?P<slug>[\w-]+)/(?P<uuid>[^/]+)/edit/$', SubmissionEdit.as_view(), name='submission_edit'),
    url(r'^(?P<slug>[\w-]+)/(?P<uuid>[^/]+)/flag/$', auth(FlagFormView.as_view()), name='flag'),
    url(r'^(?P<slug>[\w-]+)/(?P<uuid>[^/]+)/delete/$', SubmissionDelete.as_view(), name='submission_delete'),
    url(r'^(?P<slug>[\w-]+)/(?P<uuid>[^/]+)/edit/thumbnail/$',
        SubmissionEditThumbnail.as_view(),
        name='submission_edit_thumbnail'),
)

urlpatterns += format_suffix_patterns(urlpatterns)

urlpatterns += patterns(
    'django.contrib.flatpages.urls',

    # Flatpages
    url(r'^about/', flatpage, {'url': '/about/'}, name='about'),
    url(r'^privacy-policy/', flatpage, {'url': '/privacy-policy/'}, name='privacy_policy'),
    url(r'^terms-of-use/', flatpage, {'url': '/terms-of-use/'}, name='terms_of_use'),
    url(r'^rules/', flatpage, {'url': '/rules/'}, name='rules'),
    url(r'^features/', flatpage, {'url': '/features/'}, name='features'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, }),
    )
