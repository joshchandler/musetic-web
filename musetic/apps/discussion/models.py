from django.conf import settings
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.template import RequestContext
from django.template.loader import render_to_string

from .managers import DiscussionManager

from musetic.apps.submission.models import Submission


MAX_LENGTH = getattr(settings, 'DISCUSSION_MAX_LENGTH', 3000)
PATH_SEPARATOR = getattr(settings, 'DISCUSSION_PATH_SEPARATOR', '/')
PATH_DIGITS = getattr(settings, 'DISCUSSION_PATH_DIGITS', 10)


class Discussion(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='user_discussions')
    submission = models.ForeignKey(Submission, verbose_name=_('submission'), related_name='submission_discussions')
    comment = models.TextField(_('comment'), max_length=MAX_LENGTH)

    date_submitted = models.DateTimeField(_('date/time submitted'), default=timezone.now)
    date_updated = models.DateTimeField(_('date/time updated'), auto_now=True, null=True)

    is_deleted = models.BooleanField(
        _('is deleted'),
        default=False,
        help_text=_('Check this box to delete the comment')
    )

    objects = DiscussionManager()

    class Meta:
        verbose_name = _('Discussion')
        verbose_name_plural = _('Discussions')

    def __str__(self):
        return "{0}: {1} on {2}".format(self.user.username, self.comment[:50], self.submission.title)

    def get_votes(self):
        """
        Returns the number of votes associated with a particular comment
        :return: int
        """
        return self.discussion_votes.count()

    # def get_absolute_url(self, anchor_pattern="#c%(id)s"):
    #     return self.get_content_object_url() + (anchor_pattern % self.__dict__)

    def get_as_text(self):
        """
        Return this comment as plain text. Useful for emails.
        """
        d = {
            'user': self.user,
            'date': self.date_submitted,
            'comment': self.comment,
            'domain': self.site.domain,
            'url': self.get_absolute_url()
        }
        return _('Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s') % d

    def send_discussion_notification(self, site, request=None):
        """
        Sends an email to the Submitter of the Submissions
        """
        context_dict = {}
        if request is not None:
            context_dict = RequestContext(request, context_dict)
        context_dict.update({
            'user': self.user,
            'submission': self.submission,
            'comment': self.comment,
            'date_submitted': self.date_submitted,
            'site': site,
        })

        subject = render_to_string('discussion/discussion_notification_subject.txt', context_dict)
        subject = ''.join(subject.splitlines())

        message_txt = render_to_string('discussion/discussion_notification.txt', context_dict)

        email_message = EmailMultiAlternatives(
            subject,
            message_txt,
            'notifications@musetic.com',
            [self.submission.user.email]
        )

        email_message.send()


class DiscussionVote(models.Model):
    vote_type = models.BooleanField(default=True)
    discussion = models.ForeignKey(Discussion, related_name='discussion_votes')
    voter = models.ForeignKey(User, related_name='user_discussion_votes')

    def __str__(self):
        return "{0} upvoted {1} by {2}".format(
            self.voter.username,
            self.discussion.comment[:50],
            self.discussion.user.username)

    class Meta:
        db_table = 'discussion_vote'
        unique_together = (('discussion', 'voter'),)


class DiscussionFlag(models.Model):
    reason = models.CharField(_('reason'), max_length=300, db_index=True)
    flagger = models.ForeignKey(User, verbose_name=_('flagger'), related_name='discussion_flags')
    discussion = models.ForeignKey(Discussion, verbose_name=_('discussion'), related_name='flags')
    date_flagged = models.DateTimeField(_('date'), default=timezone.now)

    SUGGEST_REMOVAL = "removal suggestion"
    MODERATOR_DELETION = "moderator deletion"
    MODERATOR_APPROVAL = "moderator approval"

    class Meta:
        db_table = 'discussion_flag'
        unique_together = (('flagger', 'discussion'),)
        verbose_name = _('discussion flag')
        verbose_name_plural = _('discussion flags')

    def __str__(self):
        return "{0} flag of comment ID {1} by {2}".format(
            self.reason[:50],
            self.discussion_id,
            self.flagger.username
        )


@receiver(post_save, sender=Discussion)
def init_new_discussion(instance, created, raw, **kwargs):
    if created and not raw:
        DiscussionVote.objects.create(vote_type=True, discussion=instance, voter=instance.user)
