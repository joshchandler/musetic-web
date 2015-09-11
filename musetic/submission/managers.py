from django.db import models


class VoteCountManager(models.Manager):
    def get_query_set(self):
        return super(VoteCountManager, self).get_query_set().annotate(
            votes=models.Count('submission_votes')
        )
