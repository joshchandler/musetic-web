from musetic.tests.testcase import MuseticTestCase, MuseticApiTestCase
from django.core.urlresolvers import reverse

from musetic.apps.submission.models import Submission


class SubmissionViewTests(MuseticTestCase):

    def test_user_can_submit(self):
        response = self.client.post(reverse('submit'),
                                    {'submission_type': 'sound',
                                     'title': 'My Music',
                                     'description': 'This is my music',
                                     'url': 'http://example.com/'})

        # Get the created submission
        s = Submission.objects.get(title='My Music')
        self.assertRedirects(response, reverse('submission_detail', kwargs={'slug': s.submission_type, 'uuid': s.uuid}))

    def test_anonymous_cannot_submit(self):
        self.client.logout()
        response = self.client.post(reverse('submit'),
                                    {'submission_type': 'sound',
                                     'title': 'My Music',
                                     'description': 'This is my music',
                                     'url': 'http://example.com/'})

        self.assertRedirects(response, 'http://testserver/login/?next=/submit/',
                             status_code=302, target_status_code=200)

    def test_category_view(self):
        response = self.client.post(reverse('submit'),
                                    {'submission_type': 'sound',
                                     'title': 'My Music',
                                     'description': 'This is my music',
                                     'url': 'http://example.com/'})
        response = self.client.get(reverse('category',
                                           kwargs={'slug': 'sound'}))
        self.assertTrue(b'My Music' in response.content)
        self.assertTrue(b'foo' in response.content)

        response = self.client.get(reverse('category_new',
                                           kwargs={'slug': 'sound'}))
        self.assertTrue(b'My Music' in response.content)
        self.assertTrue(b'foo' in response.content)

        response = self.client.get(reverse('category_top',
                                           kwargs={'slug': 'sound'}))
        self.assertTrue(b'My Music' in response.content)
        self.assertTrue(b'foo' in response.content)

    def test_wrong_submission_type_in_category_views(self):
        response = self.client.get(reverse('category',
                                           kwargs={'slug': 'cat'}))
        self.assertEqual(404, response.status_code)
        response = self.client.get(reverse('category_new',
                                           kwargs={'slug': 'cat'}))
        self.assertEqual(404, response.status_code)
        response = self.client.get(reverse('category_top',
                                           kwargs={'slug': 'cat'}))
        self.assertEqual(404, response.status_code)

    # def test_wrong_submission_type_in_detail_view(self):
    #     self.client.post(reverse('submission_rules'), {'creator': True})
    #     response = self.client.post(reverse('submit'),
    #                                 {'submission_type': 'sound',
    #                                  'title': 'My Music',
    #                                  'description': 'This is my music',
    #                                  'url': 'http://example.com/'})
    #     s = Submission.objects.get(submission_type='sound', title='My Music')
    #     response = self.client.get(reverse('submission_detail',
    #                                        kwargs={'slug': 'cat', 'uuid': s.uuid}))
    #     self.assertEqual(404, response.status_code)


class SubmissionApiViewTests(MuseticApiTestCase):
    def test_api_root(self):
        self.client.get('/api/')
