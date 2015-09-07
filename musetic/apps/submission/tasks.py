import logging
from musetic import musetic_celery
from musetic.apps.submission.utils import rank_all

LOG = logging.getLogger(__name__)


class RankAllSubmissionsTask(musetic_celery.Task):
    """
    A task that will rank all submissions
    """
    def run(self):
        rank_all()
