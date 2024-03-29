from django.core.management.base import NoArgsCommand

from musetic.avatar.conf import settings
from musetic.avatar.models import Avatar


class Command(NoArgsCommand):
    help = ("Regenerates avatar thumbnails for the sizes specified in "
            "settings.AVATAR_AUTO_GENERATE_SIZES.")

    def handle_noargs(self, **options):
        for avatar in Avatar.objects.all():
            for size in settings.AVATAR_AUTO_GENERATE_SIZES:
                print("Rebuilding Avatar id=%s at size %s." % (avatar.id, size))
                avatar.create_thumbnail(size)
