import os
import hashlib
from PIL import Image

from django.db import models
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone, six
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.utils.encoding import force_bytes

from .conf import settings
from .reference import MediaTypes

from uuidfield import UUIDField


thumbnail_storage = get_storage_class(settings.SUBMISSION_STORAGE)()


def thumbnail_file_path(instance=None, filename=None, size=None, ext=None):
    tmppath = [settings.SUBMISSION_STORAGE_DIR]

    # Encode the username into UTF-8 for hashing
    # Hash the username, and create the file structure
    # Should look something like `/submissions/1/5/username/file.jpg
    user = instance.user.username
    encoding = user.encode('utf-8')
    tmp = hashlib.md5(encoding).hexdigest()
    tmppath.extend([tmp[0], tmp[1], instance.user.username])

    if not filename:
        # Filename already stored in database
        filename = instance.thumbnail.name
        if ext and settings.SUBMISSION_HASH_FILENAMES:
            (root, oldext) = os.path.splitext(filename)
            filename = root + "." + ext
    else:
        # File doesn't exist yet
        if settings.SUBMISSION_HASH_FILENAMES:
            (root, ext) = os.path.splitext(filename)
            filename = hashlib.md5(force_bytes(filename)).hexdigest()
            filename += ext
    if size:
        tmppath.extend(['resized', str(size)])
    tmppath.append(os.path.basename(filename))
    return os.path.join(*tmppath)


def find_extension(format):
    format = format.lower()
    if format == 'jpeg':
        format = 'jpg'

    return format


class VoteCountManager(models.Manager):
    def get_query_set(self):
        return super(VoteCountManager, self).get_query_set().annotate(
            votes=models.Count('submission_votes')
        )


class Submission(models.Model):
    uuid = UUIDField(auto=True, unique=True)
    submission_type = models.CharField(_('Submission Type'),
                                       max_length=255,
                                       choices=tuple([(media.name.lower(), media.value) for media in MediaTypes]),
                                       blank=False)
    title = models.CharField(_('Title'), max_length=100, blank=False)
    url = models.URLField(_('Link'), blank=False, unique=True)
    description = models.TextField(_('Description'))
    flagged = models.BooleanField(_('Is Flagged for Review'), default=False)
    user = models.ForeignKey(User, related_name='user_submissions')
    score = models.FloatField(default=0.0)
    thumbnail = models.ImageField(max_length=6144,
                                  upload_to=thumbnail_file_path,
                                  storage=thumbnail_storage,
                                  blank=True)
    date_submitted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    by_votes = VoteCountManager()
    objects = models.Manager()

    def __str__(self):
        return "{0}: {1}".format(self.submission_type, self.title)

    def get_absolute_url(self):
        return reverse('submission_detail', args=[
            str(self.submission_type),
            str(self.uuid),
        ])

    def get_votes(self):
        """
        Returns the number of votes associated with a particular submission
        :return: int
        """
        return self.submission_votes.count()

    def get_flags(self):
        """
        Return the number of flags associated with a particular submission
        :return: int
        """
        return self.submission_flags.count()

    def get_comment_count(self):
        """
        Return the number of comments associated with a particular submission
        :return: int
        """
        return self.submission_discussions.count()

    def calculate_score(self):
        """
        This is a variation of the HN ranking algorithm
        :return: score
        """
        secs_in_hour = float(60 * 60)
        g = 1.2

        delta = timezone.now() - self.date_submitted
        item_hour_age = delta.total_seconds() / secs_in_hour
        votes = self.submission_votes.count() - 1
        self.score = votes / pow((item_hour_age + 2), g)
        cached = cache.get('s{0}'.format(self.pk))
        if not cached:
            cache.set('s{0}'.format(self.pk), self.score, 30)
        self.save()
        return self.score

    def thumbnail_exists(self, size):
        return self.thumbnail.storage.exists(self.thumbnail_name(size))

    def create_thumbnail(self, size, quality=None):
        try:
            orig = self.thumbnail.storage.open(self.thumbnail.name, 'rb')
            image = Image.open(orig)
            quality = quality or settings.SUBMISSION_THUMB_QUALITY
            w, h = image.size
            if w != size or h != size:
                if w > h:
                    diff = int((w - h) / 2)
                    image = image.crop((diff, 0, w - diff, h))
                else:
                    diff = int((h - w) / 2)
                    image = image.crop((0, diff, w, h - diff))
                if image.mode != "RGB":
                    image = image.convert("RGB")
                image = image.resize((size, size), settings.SUBMISSION_RESIZE_METHOD)
                thumb = six.BytesIO()
                image.save(thumb, settings.SUBMISSION_THUMB_FORMAT, quality=quality)
                thumb_file = ContentFile(thumb.getvalue())
            else:
                thumb_file = File(orig)
            thumb = self.thumbnail.storage.save(self.thumbnail_name(size), thumb_file)
        except IOError:
            return

    def thumbnail_url(self, size):
        return self.thumbnail.storage.url(self.thumbnail_name(size))

    def thumbnail_name(self, size):
        ext = find_extension(settings.SUBMISSION_THUMB_FORMAT)
        return thumbnail_file_path(
            instance=self,
            size=size,
            ext=ext
        )


class Vote(models.Model):
    vote_type = models.BooleanField(default=True)
    submission = models.ForeignKey(Submission, related_name='submission_votes')
    voter = models.ForeignKey(User, related_name='user_votes')

    def __str__(self):
        return "%s upvoted %s by %s" % (self.voter, self.submission.title, self.submission.user)

    class Meta:
        unique_together = (('submission', 'voter'),)


class Flag(models.Model):
    reason = models.CharField(_('Reason'), max_length=300, blank=False)
    submission = models.ForeignKey(Submission, related_name='submission_flags')
    flagger = models.ForeignKey(User, related_name='user_flags')


@receiver(post_save, sender=Submission)
def init_new_submission(instance, created, raw, **kwargs):
    if created and not raw:
        Vote.objects.create(vote_type=True, submission=instance, voter=instance.user)


def remove_thumbnail_images(instance=None, **kwargs):
    for size in settings.SUBMISSION_AUTO_GENERATE_SIZES:
        if instance.thumbnail_exists(size):
            instance.submission.storage.delete(instance.thumbnail_name(size))
    instance.submission.storage.delete(instance.submission.name)


@receiver(post_save, sender=Submission)
def create_default_thumbnails(sender, instance, **kwargs):
    for size in settings.SUBMISSION_AUTO_GENERATE_SIZES:
        instance.create_thumbnail(size)
