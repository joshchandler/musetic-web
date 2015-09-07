from django.core.urlresolvers import reverse
from django.views.generic import DetailView, UpdateView
from django.http import Http404
from django.contrib.auth.models import User


from musetic.apps.user.models import Profile
from musetic.apps.user.forms import ProfileEditForm
from musetic.apps.user.serializers import ProfileSerializer
from musetic.apps.submission.models import Submission, Vote
from musetic.apps.submission.forms import FlagForm
from musetic.apps.submission.serializers import SubmissionSerializer


class ProfileBaseDetailView(DetailView):
    model = Profile
    template_name = 'user/profile.html'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super(ProfileBaseDetailView, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user__username=self.kwargs['username'])
        context["profile"] = ProfileSerializer(
            profile, context={'request': self.request}
        ).data
        context["flag_form"] = FlagForm()

        return context

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
        submissions = Submission.objects.filter(
            user__username=self.kwargs['username']
        ).order_by('-date_submitted')
        context["submissions"] = SubmissionSerializer(
            submissions, many=True, context={'request': self.request}
        ).data
        if self.request.user.is_authenticated():
            submission_in_page = [submission.pk for submission in submissions]
            context["voted"] = Vote.objects.filter(
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
        submissions = Submission.by_votes.filter(
            user__username=self.kwargs['username']
        ).order_by('-votes', '-date_submitted')
        context["submissions"] = SubmissionSerializer(
            submissions, many=True, context={'request': self.request}
        ).data

        if self.request.user.is_authenticated():
            submission_in_page = [submission.pk for submission in submissions]
            context["voted"] = Vote.objects.filter(
                voter=self.request.user
            ).filter(
                submission_id__in=submission_in_page
            ).values_list(
                'submission_id', flat=True
            )
        return context


class ProfileEdit(UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'user/profile_edit.html'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        """
        The edit profile page is not visible unless the user is activated
        """
        user = User.objects.get(username=self.kwargs['username'])
        if request.user.username == self.kwargs['username']:
            if user.is_active:
                return super(ProfileEdit, self).dispatch(request, *args, **kwargs)
        raise Http404

    def get_success_url(self):
        return reverse('user_profile', kwargs={'username': self.kwargs['username']})

    def get_context_data(self, **kwargs):
        context = super(ProfileEdit, self).get_context_data(**kwargs)
        context["edit_profile_form"] = ProfileEditForm()
        return context
