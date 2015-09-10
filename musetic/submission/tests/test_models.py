from musetic.tests.testcase import MuseticTestCase, MuseticSubmissionTestMixin
from musetic.submission.utils import rank_all


class SubmissionModelTests(MuseticSubmissionTestMixin, MuseticTestCase):

    def test_submission_and_vote_creation(self):
        """
        This only tests vote creation, because it wouldn't exist if the submission doesn't exist
        """
        vote = self.submission.submission_votes.get(voter__username='test_user')
        self.assertEquals(vote.submission.title, 'Test')
        self.assertEquals(vote.voter.username, 'test_user')

    def test_other_user_can_vote(self):
        # Count that there are 2 votes on the submission
        self.assertEquals(self.submission.get_votes(), 2)

    def test_model__str__methods(self):
        self.assertEquals(str(self.submission), 'sound: Test')
        self.assertEquals(str(self.vote2), "%s upvoted %s by %s" % (self.vote2.voter,
                                                                    self.vote2.submission.title,
                                                                    self.vote2.submission.user))

    def test_rank(self):
        """
        s is rank_all() for a single submission,
        rank_all() is here for test coverage
        """
        rank_all()
        s = self.submission.calculate_score()
        self.assertGreater(s, 0)
