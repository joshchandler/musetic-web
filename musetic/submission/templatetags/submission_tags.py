from django import template
from django.template.loader import render_to_string

from musetic.submission.conf import settings
from musetic.submission.models import Submission
from musetic.submission.utils import get_submission_thumbnail


register = template.Library()


# @cache_result
@register.simple_tag
def submission_image_url(submission, size=settings.SUBMISSION_DEFAULT_SIZE):
    submission = get_submission_thumbnail(submission, size=size)
    if submission:
        return submission.thumbnail_url(size)
    return


# @cache_result
@register.simple_tag
def submission_image(submission, size=settings.SUBMISSION_DEFAULT_SIZE, **kwargs):
    submission = Submission.objects.get(url=submission)
    url = submission_image_url(submission, size)

    context = dict(kwargs, **{
        'submission': submission,
        'url': url,
        'size': size,
    })
    return render_to_string('submission/thumbnail_tag.html', context)
