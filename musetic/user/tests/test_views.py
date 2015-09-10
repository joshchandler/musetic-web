from django.core.urlresolvers import reverse
from django.core import mail
from django.test import TestCase

from musetic.tests.testcase import MuseticTestCase
from musetic.user.models import Profile, Creator

from registration.models import RegistrationProfile


class UserRegistrationViewTests(TestCase):
    """
    Test the default registration backend.

    Running these tests successfully will require two templates to be
    created for the sending of activation emails; details on these
    templates and their contexts may be found in the documentation for
    the default backend.

    """
    def test_user_profile_page(self):
        """
        Test user has a profile page upon activation

        """
        response = self.client.post(reverse('registration_register'),
                                    {'username': 'bob',
                                     'email': 'bob@example.com',
                                     'password1': 'secret',
                                     'password2': 'secret'})

        # Activate the new account
        profile = RegistrationProfile.objects.get(user__username='bob')
        response = self.client.get(reverse('registration_activate',
                                           args=(),
                                           kwargs={'activation_key': profile.activation_key}))
        self.assertRedirects(response, reverse('index'))

        # User can now view their profile
        response = self.client.get(reverse('user_profile',
                                           kwargs={'username': 'bob'}))
        self.assertEqual(200, response.status_code)

    def test_user_profile_page_failure(self):
        """
        User must be active to have a profile page
        """
        response = self.client.post(reverse('registration_register'),
                                    {'username': 'bob',
                                     'email': 'bob@example.com',
                                     'password1': 'secret',
                                     'password2': 'secret'})

        response = self.client.get(reverse('user_profile',
                                           kwargs={'username': 'bob'}))
        self.assertEqual(404, response.status_code)

        response = self.client.get(reverse('edit_profile',
                                           kwargs={'username': 'bob'}))
        self.assertEqual(302, response.status_code)


class UserViewTests(MuseticTestCase):
    """
    Test the users that are registered already.

    """

    def test_login(self):
        self.client.logout()
        # Go to the login page
        response = self.client.get('/login/')
        self.assertTrue(b'Log in' in response.content)

        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/')
        self.assertTrue(b'foo' in response.content)

    def test_logout(self):

        response = self.client.get('/')
        self.assertTrue(b'Logout' in response.content)

        self.client.logout()

        response = self.client.get('/')
        self.assertTrue(b'Login' in response.content)

    def test_registration_view(self):
        response = self.client.post(reverse('registration_register'),
                                    {'username': self.username,
                                     'email': self.admin.email,
                                     'password1': self.password,
                                     'password2': self.password})
        self.assertEquals(response.status_code, 302)

    def test_anonymous_users_can_view_profiles(self):

        self.client.logout()
        # Make sure no user is signed in
        response = self.client.get('/')
        self.assertTrue(b'Login' in response.content)

        # View the user's profile
        response = self.client.get('/muser/foo/')
        self.assertTrue(b'foo' in response.content)

    def test_anonymous_users_cannot_edit_profiles(self):

        self.client.logout()
        # Make sure no user is signed in
        response = self.client.get('/')
        self.assertTrue(b'Login' in response.content)

        # Try to edit user's profile, but redirect to the login page
        response = self.client.get('/muser/foo/edit/')
        self.assertEquals(response.status_code, 302)

    def test_superuser_can_view_profile_without_activation(self):
        response = self.client.get(reverse('user_profile',
                                           kwargs={'username': self.username}))
        self.assertTrue(b'foo' in response.content)

    def test_user_can_edit_profile(self):
        self.client.post(reverse('edit_profile', kwargs={'username': self.username}),
                         {'description': 'This is my description',
                          'first_name': 'Admin',
                          'last_name': 'User'})
        u = Profile.objects.get(user__username=self.username)
        self.assertEquals(u.description, 'This is my description')
        self.assertEquals(u.user.first_name, 'Admin')
        self.assertEquals(u.user.last_name, 'User')

    def test_creator_request_and_activate(self):
        self.client.logout()
        self.client.login(username='test', password='password')
        response = self.client.post(reverse('creator_request'),
                                    {'url': 'http://test-website.com'})
        self.assertRedirects(response, reverse('creator_request_sent'))

        # Must account for the admin's creator account
        self.assertEqual(Creator.objects.count(), 2)
        self.assertEqual(len(mail.outbox), 1)

        self.client.logout()
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(reverse('creator_accept', kwargs={'username': 'test'}))

        self.assertRedirects(response, reverse('creator_activated', kwargs={'username': 'test'}))

        new_creator = Creator.objects.get(user__username='test')

        # Remember the first email, it's still there
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(new_creator.is_creator, True)
