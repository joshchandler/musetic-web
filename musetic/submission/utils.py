import hashlib

from django.core.cache import cache
from django.utils import six
from django.template.defaultfilters import slugify
from django.utils.encoding import force_bytes

from .models import Submission
from .conf import settings


def rank_all():
    for submission in Submission.objects.all():
        submission.calculate_score()


cached_funcs = set()


def get_submissionurl(submission):
    return submission.url


def get_submission(submissionurl):
    return Submission.objects.get(url=submissionurl)


def get_cache_key(submissionurl, size, prefix):
    submissionurl = get_submissionurl(submissionurl)
    key = six.u('%s_%s_%s') % (prefix, submissionurl, size)
    return six.u('%s_%s') % (slugify(key)[:100],
                             hashlib.md5(force_bytes(key)).hexdigest())


def cache_set(key, value):
    cache.set(key, value, settings.SUBMISSION_CACHE_TIMEOUT)


def cache_result(default_size=settings.SUBMISSION_DEFAULT_SIZE):

    def decorator(func):
        def cached_func(submissionurl, size=None):
            prefix = func.__name__
            cached_funcs.add(prefix)
            key = get_cache_key(submissionurl, size or default_size, prefix=prefix)
            result = cache.get(key)
            if result is None:
                result = func(submissionurl, size or default_size)
                cache_set(key, result)
            return result
        return cached_func
    return decorator


def invalidate_cache(submissionurl, size=None):
    sizes = set(settings.SUBMISSION_AUTO_GENERATE_SIZES)
    if size is not None:
        sizes.add(size)
    for prefix in cached_funcs:
        for size in sizes:
            cache.delete(get_cache_key(submissionurl, size, prefix))


def get_submission_thumbnail(submission, size=settings.SUBMISSION_DEFAULT_SIZE):
    submission = Submission.objects.get(url=submission.url)

    if submission:
        if not submission.thumbnail_exists(size):
            submission.create_thumbnail(size)
    return submission
