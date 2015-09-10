from django.conf import settings
from PIL import Image

from appconf import AppConf


class SubmissionConf(AppConf):
    DEFAULT_SIZE = 500
    RESIZE_METHOD = Image.ANTIALIAS
    STORAGE_DIR = 'submissions'
    MAX_SIZE = 6144 * 6144
    THUMB_FORMAT = 'JPEG'
    THUMB_QUALITY = 85
    HASH_FILENAMES = True
    HASH_USERDIRNAMES = True
    ALLOWED_FILE_EXTS = ('.jpg', '.jpeg', '.png',)
    CACHE_TIMEOUT = 60 * 60
    STORAGE = settings.DEFAULT_FILE_STORAGE
    CLEANUP_DELETED = True
    AUTO_GENERATE_SIZES = (DEFAULT_SIZE,)

    def configure_auto_generate_thumbnail_sizes(self, value):
        return value or getattr(settings, 'AUTO_GENERATE_SUBMISSION_SIZES',
                                (self.DEFAULT_SIZE,))
