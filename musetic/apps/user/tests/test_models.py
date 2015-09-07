from musetic.tests.testcase import MuseticTestCase, MuseticSubmissionTestMixin
from musetic.apps.user.models import Profile, Creator, Feedback


class ProfileModelTests(MuseticSubmissionTestMixin, MuseticTestCase):

    def test_profile_creation(self):
        profile = Profile.objects.get(user__username=self.reg_user.username)
        self.assertEquals(profile.get_absolute_url(), '/muser/test_user/')

    def test__str__methods(self):
        profile = Profile.objects.get(user__username=self.reg_user.username)
        self.assertEquals(str(profile), 'test_user')

    def test_profile_score_method(self):
        profile = Profile.objects.get(user__username=self.reg_user.username)
        self.assertEquals(profile.score(), 2)


class CreatorModelTests(MuseticTestCase):

    def test__str__methods(self):
        creator = Creator.objects.get(user__username=self.username)
        self.assertEquals(str(creator), 'foo: True')


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
