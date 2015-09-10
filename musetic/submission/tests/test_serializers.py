from musetic.tests.testcase import MuseticSubmissionTestMixin, MuseticTestCase
from musetic.submission.serializers import SubmissionSerializer, VoteSerializer


class SubmissionSerializerTests(MuseticSubmissionTestMixin, MuseticTestCase):

    def test_submission_serialized_data(self):
        data = SubmissionSerializer(self.submission).data

        self.assertEquals('sound', data['submission_type'])
        self.assertEquals('Test', data['title'])
        self.assertEquals('http://example.com/', data['url'])

    # def test_rank_method(self):
        # data = SubmissionSerializer(self.submission).data
        # self.assertGreater(data['score'], 0)

    def test_get_votes_method(self):
        data = SubmissionSerializer(self.submission)
        self.assertEquals(2, data.get_votes(self.submission))


class VoteSerializerTests(MuseticSubmissionTestMixin, MuseticTestCase):

    def test_vote_serialized_data(self):
        data = VoteSerializer(self.vote2).data

        self.assertEquals('sound', data['submission']['submission_type'])
        self.assertEquals('admin_test_user', data['voter']['username'])
