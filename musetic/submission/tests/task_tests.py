import logging

from mock import patch
from django.test import TestCase

from musetic.submission.tasks import RankAllSubmissionsTask

logging.disable(logging.CRITICAL)


class RankAllSubmissionsTaskTests(TestCase):
    """
    Tests for RankAllSubmissionsTask
    """
    @patch('musetic.submission.tasks.rank_all')
    def test_run(self, mock_rank_all):
        """
        Test that .run() calls rank_all()
        """
        RankAllSubmissionsTask().run()

        mock_rank_all.assert_called_once_with()
