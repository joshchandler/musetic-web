from django.db import models


class DiscussionManager(models.Manager):
    def get_query_set(self):
        return super(DiscussionManager, self).get_query_set().annotate(
            votes=models.Count('discussion_votes')
        )

    def create_comment(self, user, submission, comment, date_submitted, site, send_email=True, request=None):
        """
        Creates a new comment entry, and emails the new comment to the OP
        """
        comment = self.create(user=user, submission=submission, comment=comment, date_submitted=date_submitted)

        if send_email:
            comment.send_discussion_notification(site, request)

        return comment
