from django.core.management.base import BaseCommand
from musetic.apps.submission.models import Submission
from musetic.apps.submission.utils import rank_all
import time


class Command(BaseCommand):
    def handle(self, *args, **command):
        while 1:
            print("---"*15)
            rank_all()
            self.show_all()
            time.sleep(30)

    def show_all(self):
        print("\n".join(
            ["{0}".format(s.calculate_score()) for s in Submission.objects.all()]
        ))
        print("---"*15 + "\n\n")
