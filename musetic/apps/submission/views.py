import json
from django.views.generic import ListView, CreateView, DetailView, FormView, UpdateView, DeleteView
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, redirect
from django.db import models

from .forms import SubmissionForm, SubmissionEditForm, SubmissionEditThumbnailForm, VoteForm, FlagForm
from .models import Submission, Vote, Flag
from .reference import MediaTypes
from .serializers import SubmissionSerializer, PaginatedSubmissionSerializer
from musetic.apps.user.models import Creator, User
from musetic.apps.discussion.models import Discussion, DiscussionVote
from musetic.apps.discussion.forms import DiscussionForm
from braces.views import LoginRequiredMixin


class SubmissionBaseList(ListView):
    template_name = 'submission/list.html'
    model = Submission
    paginate_by = 12

    def paginate_submissions(self, queryset, paginate_by):
        """
        Paginate the queryset, then serialize the submission data using a PaginationSerializer
        """
        paginator = Paginator(queryset, paginate_by)
        page = self.request.GET.get('page')
        try:
            submissions = paginator.page(page)
        except PageNotAnInteger:
            submissions = paginator.page(1)
        except EmptyPage:
            submissions = paginator.page(paginator.num_pages)

        return PaginatedSubmissionSerializer(submissions, context={'request': self.request}).data

    def get_context_data(self, **kwargs):
        context = super(SubmissionBaseList, self).get_context_data(**kwargs)
        pagination = self.paginate_submissions(self.get_queryset(), self.paginate_by)
        submissions = pagination.get("results")
        context["submissions"] = submissions
        context["pagination"] = pagination

        if self.request.user.is_authenticated():
            submission_in_page = [submission.pk for submission in context["object_list"]]
            context["voted"] = Vote.objects.filter(
                voter=self.request.user
            ).filter(
                submission_id__in=submission_in_page
            ).values_list(
                'submission_id', flat=True
            )

        return context


class SubmissionHotList(SubmissionBaseList):
    queryset = Submission.by_votes.order_by('-score', '-votes', '-date_submitted')


class SubmissionNewList(SubmissionBaseList):
    queryset = Submission.objects.order_by('-date_submitted')


class SubmissionTopList(SubmissionBaseList):
    queryset = Submission.by_votes.order_by('-votes', '-date_submitted')


class SubmissionCategoryBaseList(SubmissionBaseList):
    """
    Base View Class for Submissions that are filtered by category
    """
    template_name = 'submission/category_list.html'
    MEDIA_TYPES = [media.value for media in MediaTypes]

    def get_context_data(self, **kwargs):
        context = super(SubmissionCategoryBaseList, self).get_context_data(**kwargs)
        context['submission_type'] = self.kwargs['slug']
        return context


class SubmissionCategoryHotList(SubmissionCategoryBaseList):

    def get_queryset(self):
        if self.kwargs['slug'] in self.MEDIA_TYPES:
            return super(SubmissionCategoryHotList, self).get_queryset().filter(
                submission_type=self.kwargs['slug']
            ).order_by(
                '-score', '-votes', '-date_submitted'
            )
        raise Http404


class SubmissionCategoryNewList(SubmissionCategoryBaseList):

    def get_queryset(self):
        if self.kwargs['slug'] in self.MEDIA_TYPES:
            return super(SubmissionCategoryNewList, self).get_queryset().filter(
                submission_type=self.kwargs['slug']
            ).order_by('-date_submitted')
        raise Http404


class SubmissionCategoryTopList(SubmissionCategoryBaseList):

    def get_queryset(self):
        if self.kwargs['slug'] in self.MEDIA_TYPES:
            return super(SubmissionCategoryTopList, self).get_queryset().annotate(
                votes=models.Count('submission_votes')
            ).filter(
                submission_type=self.kwargs['slug']
            ).order_by(
                '-votes', '-date_submitted'
            )
        raise Http404


class SubmissionDetail(DetailView):
    model = Submission
    template_name = 'submission/detail.html'
    MEDIA_TYPES = [media.value for media in MediaTypes]

    def get_object(self, queryset=None):
        return Submission.objects.get(submission_type=self.kwargs['slug'], uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(SubmissionDetail, self).get_context_data(**kwargs)
        submission = Submission.objects.get(submission_type=self.kwargs['slug'], uuid=self.kwargs['uuid'])
        context['submission_type'] = self.kwargs['slug']
        context["submission"] = SubmissionSerializer(
            submission, context={'request': self.request}
        ).data
        context["profile"] = User.objects.get(user_submissions=submission)
        context["discussion_form"] = DiscussionForm()
        discussions = Discussion.objects.filter(
            submission__uuid=self.kwargs['uuid']
        ).order_by('-date_submitted')
        context["discussions"] = discussions

        if self.request.user.is_authenticated():
            context["voted"] = Vote.objects.filter(
                voter=self.request.user
            ).filter(
                submission_id=submission.id
            ).values_list(
                'submission_id', flat=True
            )
            context["flagged"] = Flag.objects.filter(
                flagger=self.request.user
            ).filter(
                submission_id=submission.id
            ).values_list(
                'submission_id', flat=True
            )
            discussion_in_page = [discussion.id for discussion in discussions]
            context["discussion_voted"] = DiscussionVote.objects.filter(
                voter=self.request.user
            ).filter(
                discussion_id__in=discussion_in_page
            ).values_list(
                'discussion_id', flat=True
            )

        return context

    def get_queryset(self):
        if self.kwargs['slug'] in self.MEDIA_TYPES:
            queryset = super(SubmissionDetail, self).get_queryset()
            return queryset.filter(submission_type=self.kwargs['slug'])
        raise Http404


class SubmissionCreate(CreateView):
    """
    Displays the form where users can submit their work
    """
    form_class = SubmissionForm
    model = Submission
    template_name = 'submission/submit.html'

    def dispatch(self, request, *args, **kwargs):
        creator = Creator.objects.get(user_id=request.user.id)
        if not creator.is_creator:
            return redirect(reverse('submission_rules'))
        return super(SubmissionCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SubmissionCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SubmissionCreate, self).get_context_data(**kwargs)
        context['submission_form'] = SubmissionForm()
        return context


class SubmissionEdit(LoginRequiredMixin, UpdateView):
    model = Submission
    template_name = 'submission/edit.html'
    form_class = SubmissionEditForm

    def get_object(self, queryset=None):
        return Submission.objects.get(submission_type=self.kwargs['slug'], uuid=self.kwargs['uuid'])

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        submission = Submission.objects.get(uuid=self.kwargs['uuid'])
        if user.username == submission.user.username or user.is_staff:
            return super(SubmissionEdit, self).dispatch(request, *args, **kwargs)
        raise Http404

    def get_success_url(self):
        return reverse('submission_detail', kwargs={'slug': self.kwargs['slug'], 'uuid': self.kwargs['uuid']})

    def get_context_data(self, **kwargs):
        context = super(SubmissionEdit, self).get_context_data(**kwargs)
        return context


class SubmissionDelete(LoginRequiredMixin, DeleteView):
    model = Submission
    template_name = 'submission/delete.html'

    def get_object(self, queryset=None):
        return Submission.objects.get(submission_type=self.kwargs['slug'], uuid=self.kwargs['uuid'])

    def get_success_url(self):
        return reverse('user_profile', kwargs={'username': self.request.user.username})


class SubmissionEditThumbnail(LoginRequiredMixin, UpdateView):
    model = Submission
    template_name = 'submission/edit_thumbnail.html'
    form_class = SubmissionEditThumbnailForm

    def get_object(self, queryset=None):
        return Submission.objects.get(submission_type=self.kwargs['slug'], uuid=self.kwargs['uuid'])

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        submission = Submission.objects.get(uuid=self.kwargs['uuid'])
        if user.username == submission.user.username:
            return super(SubmissionEditThumbnail, self).dispatch(request, *args, **kwargs)
        raise Http404

    def get_success_url(self):
        return reverse('submission_detail', kwargs={'slug': self.kwargs['slug'], 'uuid': self.kwargs['uuid']})

    def get_context_data(self, **kwargs):
        context = super(SubmissionEditThumbnail, self).get_context_data(**kwargs)
        context["submission_edit_thumbnail_form"] = SubmissionEditThumbnailForm()
        return context


class JSONFormMixin(object):
    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response


class VoteFormBaseView(FormView):
    form_class = VoteForm

    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response

    def form_valid(self, form):
        """
        If a user has not already voted on a submission, create the vote.
        If a user has already voted, then the vote is deleted
        """
        submission = get_object_or_404(Submission, pk=form.data["submission"])
        user = self.request.user
        vote = Vote.objects.filter(submission=submission, voter=user)
        already_voted = bool(len(vote) > 0)

        ret = {"success": 1}
        if not already_voted:
            v = Vote.objects.create(submission=submission, voter=user)
            ret['voteobj'] = v.id
        else:
            # Doesn't work this way
            vote[0].delete()
            ret["unvoted"] = 1
        return self.create_response(ret, True)

    def form_invalid(self, form):
        ret = {"success": 0, "form_errors": form.errors}
        return self.create_response(ret, False)


class VoteFormView(JSONFormMixin, VoteFormBaseView):
    pass


class FlagFormView(FormView):
    template_name = 'submission/flag.html'
    form_class = FlagForm
    model = Flag

    def get_context_data(self, **kwargs):
        context = super(FlagFormView, self).get_context_data(**kwargs)
        context["submission"] = Submission.objects.get(submission_type=self.kwargs['slug'], uuid=self.kwargs['uuid'])
        return context

    def get_success_url(self):
        return reverse('submission_detail', kwargs={'slug': self.kwargs['slug'], 'uuid': self.kwargs['uuid']})

    def form_valid(self, form):
        form.instance.flagger = self.request.user
        form.instance.submission = Submission.objects.get(submission_type=self.kwargs['slug'], uuid=self.kwargs['uuid'])
        form.save()
        return super(FlagFormView, self).form_valid(form)
