import logging

from mock import patch
from django.test import TestCase

from musetic.apps.submission.tasks import RankAllSubmissionsTask

logging.disable(logging.CRITICAL)


class RankAllSubmissionsTaskTests(TestCase):
    """
    Tests for RankAllSubmissionsTask
    """
    @patch('musetic.apps.submission.tasks.rank_all')
    def test_run(self, mock_rank_all):
        """
        Test that .run() calls rank_all()
        """
        RankAllSubmissionsTask().run()

        mock_rank_all.assert_called_once_with()
