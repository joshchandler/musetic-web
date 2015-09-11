from django.test import TestCase

from musetic.user.models import User, Creator
from musetic.submission.models import Submission, Vote

from django_dynamic_fixture import G
from registration.models import RegistrationProfile
from rest_framework.test import APIClient


class MuseticTestCase(TestCase):

    def setUp(self):
        super(MuseticTestCase, self).setUp()
        self.username = 'foo'
        self.password = 'bar'
        self.admin = User.objects.create_superuser(
            email='admin@musetic.com',
            username=self.username,
            password=self.password
        )
        self.creator = Creator.objects.create(
            user=self.admin,
            url='http://foo.bar',
            is_creator=True
        )

        self.non_admin = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='password'
        )
        self.non_admin_registered = RegistrationProfile.objects.create(
            user=self.non_admin,
            activation_key='ALREADY_ACTIVATED'
        )
        self.non_admin = User.objects.get(username='test')
        self.client.login(username=self.username, password=self.password)


class MuseticApiTestCase(MuseticTestCase):
    client_class = APIClient


class MuseticSubmissionTestMixin(object):

    def setUp(self):
        self.reg_user = User.objects.create_user(username='test_user', email='test@example.com', password='password')
        self.admin = User.objects.create_superuser(
            username='admin_test_user', email='admin@musetic.com', password='password'
        )
        self.submission = G(Submission,
                            submission_type='sound',
                            title='Test',
                            description='Some of my music',
                            user=self.reg_user,
                            url='http://example.com/',
                            uuid='6b8500f0-594d-11e4-8ed6-0800200c9a66')

        self.vote2 = G(Vote,
                       submission=self.submission,
                       voter=self.admin)
