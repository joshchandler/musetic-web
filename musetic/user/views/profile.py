from django.views.generic import DetailView
from django.http import Http404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from musetic.user.models import Profile

from musetic.submission.models import Submission, Vote


class ProfileBaseDetailView(DetailView):
    model = Profile
    template_name = 'user/profile.html'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'

    def paginate_submissions(self, queryset, paginate_by):
        """
        Paginate the queryset
        """
        paginator = Paginator(queryset, paginate_by)
        page = self.request.GET.get('page')
        try:
            submissions = paginator.page(page)
        except PageNotAnInteger:
            submissions = paginator.page(1)
        except EmptyPage:
            submissions = paginator.page(paginator.num_pages)

        return submissions

    def dispatch(self, request, *args, **kwargs):
        """
        The profile page is not visible unless the user is activated
        """
        user = User.objects.get(username=self.kwargs['username'])
        if user.is_active:
            return super(ProfileBaseDetailView, self).dispatch(request, *args, **kwargs)
        raise Http404


class ProfileNewDetailView(ProfileBaseDetailView):
    def get_context_data(self, **kwargs):
        context = super(ProfileNewDetailView, self).get_context_data(**kwargs)
        context["submissions"] = self.paginate_submissions(
            Submission.by_votes.select_related().filter(
                user__username=self.kwargs['username']
            ).order_by('-date_submitted'), paginate_by=12)

        if self.request.user.is_authenticated():
            submission_in_page = [submission.pk for submission in context["submissions"]]
            context["voted"] = Vote.objects.select_related().filter(
                voter=self.request.user
            ).filter(
                submission_id__in=submission_in_page
            ).values_list(
                'submission_id', flat=True
            )
        return context


class ProfileTopDetailView(ProfileBaseDetailView):
    def get_context_data(self, **kwargs):
        context = super(ProfileTopDetailView, self).get_context_data(**kwargs)
        context["submissions"] = self.paginate_submissions(
            Submission.by_votes.select_related().filter(
                user__username=self.kwargs['username']
            ).order_by('-votes', '-date_submitted'), paginate_by=12)

        if self.request.user.is_authenticated():
            submission_in_page = [submission.pk for submission in context["submissions"]]
            context["voted"] = Vote.objects.select_related().filter(
                voter=self.request.user
            ).filter(
                submission_id__in=submission_in_page
            ).values_list(
                'submission_id', flat=True
            )
        return context
