from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.template.loader import render_to_string

from .managers import CreatorManager, InviteManager

from musetic.discussion.models import Discussion, DiscussionVote
from musetic.submission.models import Submission, Vote


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    description = models.TextField(null=True, blank=True, verbose_name="Write something about yourself!")

    class Meta:
        db_table = 'user_userprofile'

    def __str__(self):
        return str(self.user.username)

    def score(self):
        """
        Returns the total amount of votes associated with all of the
        submissions a particular user has submitted
        :return: int
        """
        submissions = Submission.objects.filter(user=self.user)
        score = 0
        for submission in submissions:
            votes = Vote.objects.filter(submission=submission)
            num_votes = votes.count()
            score += num_votes
        return score

    def discussion_score(self):
        """
        Returns the total amount of votes associated with all of the
        comments a particular user has submitted
        :return: int
        """
        discussions = Discussion.objects.filter(user=self.user)
        score = 0
        for discussion in discussions:
            votes = DiscussionVote.objects.filter(discussion=discussion)
            num_votes = votes.count()
            score += num_votes
        return score

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'username': self.user.username})


class Creator(models.Model):
    user = models.OneToOneField(User, related_name='creator')
    url = models.URLField(_('Link to your Work'), blank=False, unique=True)
    is_creator = models.BooleanField(_('is creator'), default=False)

    objects = CreatorManager()

    class Meta:
        db_table = 'user_usercreator'

    def __str__(self):
        return str(self.user.username) + ': ' + str(self.is_creator)

    def send_creator_request_email(self, site, request=None):
        """
        Send an email to join@musetic.com

        This makes use of two templates:
        `user/email_creator_request_subject.txt` which contains the subject of the email,
        and `user/email_creator_request.txt` which contains the email message

        This email must contain the user information, the url in this model, and the
        site's domain name.
        """
        admins = User.objects.all().filter(is_staff=True)
        admin_email_list = []
        for admin in admins:
            admin_email_list.append(admin.email)
            
        context_dict = {}
        if request is not None:
            context_dict = RequestContext(request, context_dict)
        context_dict.update({
            'user': self.user,
            'url': self.url,
            'site': site,
        })

        subject = render_to_string('email/user/creator_request_subject.txt', context_dict)
        subject = ''.join(subject.splitlines())

        message_txt = render_to_string('email/user/creator_request.txt', context_dict)
        email_message = EmailMultiAlternatives(subject, message_txt, settings.DEFAULT_FROM_EMAIL, admin_email_list)

        email_message.send()

    def send_acceptance_email(self, site, request=None):
        """
        Sends an email to the muser with a newly accepted creator account
        """
        context_dict = {}
        if request is not None:
            context_dict = RequestContext(request, context_dict)
        context_dict.update({
            'user': self.user,
            'site': site,
        })

        subject = render_to_string('email/user/acceptance_email_subject.txt', context_dict)
        subject = ''.join(subject.splitlines())

        message_txt = render_to_string('email/user/acceptance_email.txt', context_dict)
        email_message = EmailMultiAlternatives(subject, message_txt, settings.DEFAULT_FROM_EMAIL, [self.user.email])

        email_message.send()


class Invite(models.Model):
    inviter = models.ForeignKey(User, related_name='user_inviter')
    activation_key = models.CharField(_('activation key'), max_length=40)
    invitee = models.EmailField(_('invitee email address'), unique=True)
    date_invited = models.DateTimeField(_('date invited'), default=timezone.now)
    accepted = models.BooleanField(_('accepted'), default=False)

    LIMIT = 5

    objects = InviteManager()

    class Meta:
        db_table = 'user_userinvite'
        unique_together = (("inviter", "invitee"),)

    def __str__(self):
        return "{0} invited {1}".format(self.inviter.username, self.invitee)

    def send_invitation_email(self, site, request=None):
        ctx_dict = {}
        if request is not None:
            ctx_dict = RequestContext(request, ctx_dict)  # pragma: no cover
        ctx_dict.update({
            'inviter': self.inviter,
            'activation_key': self.activation_key,
            'invitee': self.invitee,
            'site': site,
        })
        subject = render_to_string('email/user/invitation_email_subject.txt', ctx_dict)
        subject = ''.join(subject.splitlines())

        message_txt = render_to_string('email/user/invitation_email.txt', ctx_dict)
        email_message = EmailMultiAlternatives(subject, message_txt, settings.DEFAULT_FROM_EMAIL, [self.invitee])

        email_message.send()

    def send_invite_accepted_email(self, new_user, site, request=None):
        ctx_dict = {}
        if request is not None:
            ctx_dict = RequestContext(request, ctx_dict)  # pragma: no cover
        ctx_dict.update({
            'inviter': self.inviter,
            'new_user': new_user,
            'site': site,
        })
        subject = render_to_string('email/user/invitation_accepted_subject.txt', ctx_dict)
        subject = ''.join(subject.splitlines())

        message_txt = render_to_string('email/user/invitation_accepted.txt', ctx_dict)
        email_message = EmailMultiAlternatives(subject, message_txt, settings.DEFAULT_FROM_EMAIL, [self.inviter.email])
        # message_html = render_to_string('emails/user/invitation_accepted.html', ctx_dict)
        # email_message.attach_alternative(message_html, 'text/html')

        email_message.send()


class Feedback(models.Model):
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    email = models.EmailField(_('email address'), null=True)
    subject = models.CharField(blank=False, max_length=300)
    body = models.TextField(blank=False, max_length=2000, null=False)

    class Meta:
        db_table = 'user_userfeedback'
        verbose_name = 'feedback'
        verbose_name_plural = 'feedback'

    def __str__(self):
        return str(self.email) + ' writes ' + str(self.subject)


class Settings(models.Model):
    user = models.OneToOneField(User, related_name='user_settings')

    show_feedback_tab = models.BooleanField(default=True)
    mail_comment_notifications = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_usersettings'


@receiver(post_save, sender=User)
def init_new_user(instance, created, raw, **kwargs):
    if created and not raw:
        Profile.objects.create(description='', user=instance)
        Settings.objects.create(user=instance)
