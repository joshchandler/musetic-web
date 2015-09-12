from django.core import mail

from musetic.tests.testcase import MuseticTestCase, SubmissionTestMixin
from musetic.user.models import User, Profile, Creator, Feedback, Invite
from musetic.discussion.models import Discussion, DiscussionVote
from musetic.submission.models import Submission

from django_dynamic_fixture import G


class ProfileModelTests(SubmissionTestMixin, MuseticTestCase):
    def test_profile_creation(self):
        profile = Profile.objects.get(user__username=self.reg_user.username)
        self.assertEquals(profile.get_absolute_url(), '/muser/test_user/')

    def test__str__methods(self):
        profile = Profile.objects.get(user__username=self.reg_user.username)
        self.assertEquals(str(profile), 'test_user')

    def test_profile_score_method(self):
        profile = Profile.objects.get(user__username=self.reg_user.username)
        self.assertEquals(profile.score(), 2)

    def test_profile_discussion_score_method(self):
        user = G(User)
        user2 = G(User)
        creator = G(Creator, user=user, is_creator=True)
        submission = G(Submission, user=user)
        discussion = G(Discussion, submission=submission, user=user2)
        vote = G(DiscussionVote, voter=user, discussion=discussion)
        profile = Profile.objects.get(user__username=user2.username)
        self.assertEquals(profile.discussion_score(), 2)


class CreatorModelTests(MuseticTestCase):
    def test__str__methods(self):
        creator = Creator.objects.get(user__username=self.username)
        self.assertEquals(str(creator), 'foo: True')


class InviteModelTests(MuseticTestCase):
    def test__str__methods(self):
        user = G(User, username='test_example')
        invite = G(Invite, inviter=user, invitee='test@example.com')
        self.assertEquals(str(invite), 'test_example invited test@example.com')

    def test_send_invitation_email(self):
        invite = G(Invite)
        invite.send_invitation_email('musetic.com')
        self.assertEquals(len(mail.outbox), 1)
    
    def test_send_invite_accepted_email(self):
        invite = G(Invite)
        new_user = G(User)
        invite.send_invite_accepted_email(new_user, 'musetic.com')
        self.assertEquals(len(mail.outbox), 1)


class FeedbackModelTests(MuseticTestCase):
    def test_feedback_creator(self):
        feedback = Feedback.objects.create(email=self.admin.email,
                                           subject='Design',
                                           body='It needs to pop a little more')
        self.assertEquals(feedback.subject, 'Design')

    def test__str__methods(self):
        Feedback.objects.create(email=self.admin.email,
                                subject='Design',
                                body='It needs to pop a little more')

        feedback = Feedback.objects.get(email=self.admin.email, subject='Design')
        self.assertEquals(str(feedback), 'admin@musetic.com writes Design')
