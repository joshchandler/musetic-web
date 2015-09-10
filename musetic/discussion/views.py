import json
from django.views.generic import FormView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.sites.models import RequestSite
from django.shortcuts import get_object_or_404

from .forms import DiscussionForm, DiscussionVoteForm, DiscussionFlagForm, DiscussionEditForm
from .models import Discussion, DiscussionVote, DiscussionFlag
from musetic.discussion import signals

from musetic.submission.models import Submission

from registration.views import _RequestPassingFormView
from braces.views import LoginRequiredMixin


class DiscussionFormView(_RequestPassingFormView):
    template_name = 'discussion/discussion_form.html'
    form_class = DiscussionForm
    model = Discussion
    http_method_names = ['get', 'post', 'head', 'options', 'trace']

    def get_context_data(self, **kwargs):
        context = super(DiscussionFormView, self).get_context_data(**kwargs)
        context["submission"] = Submission.objects.get(submission_type=self.kwargs['slug'], uuid=self.kwargs['uuid'])
        return context

    def get_success_url(self, request, user):
        return reverse('submission_detail', kwargs={'slug': self.kwargs['slug'], 'uuid': self.kwargs['uuid']})

    def form_valid(self, request, form):
        comment = self.create_comment(self.request, **form.cleaned_data)
        success_url = self.get_success_url(request, comment)

        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(success_url)

    def create_comment(self, request, **cleaned_data):
        """

        """
        user = self.request.user
        submission = Submission.objects.get(submission_type=self.kwargs['slug'], uuid=self.kwargs['uuid'])
        comment = cleaned_data['comment']
        date_submitted = timezone.now()
        site = RequestSite(request)

        if submission.user.username == user.username:
            send_email = False
        else:
            send_email = True

        new_comment = Discussion.objects.create_comment(
            user,
            submission,
            comment,
            date_submitted,
            site,
            send_email,
            request=request,
        )

        signals.comment_created.send(sender=self.__class__,
                                     comment=new_comment,
                                     request=request)

        return new_comment


class DiscussionEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Discussion
    template_name = 'discussion/edit.html'
    form_class = DiscussionEditForm
    success_message = 'Your comment has been updated'

    def get_object(self, queryset=None):
        submission = Submission.objects.get(submission_type=self.kwargs['slug'], uuid=self.kwargs['uuid'])
        return Discussion.objects.get(submission=submission, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(DiscussionEdit, self).get_context_data(**kwargs)
        context["submission"] = Submission.objects.get(submission_type=self.kwargs['slug'], uuid=self.kwargs['uuid'])
        return context

    def get_success_url(self):
        return reverse('submission_detail', kwargs={'slug': self.kwargs['slug'], 'uuid': self.kwargs['uuid']})


class DiscussionDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Discussion
    template_name = 'discussion/delete.html'
    success_message = 'Your comment has been deleted'

    def get_object(self, queryset=None):
        submission = Submission.objects.get(submission_type=self.kwargs['slug'], uuid=self.kwargs['uuid'])
        return Discussion.objects.get(submission=submission, pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DiscussionDelete, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DiscussionDelete, self).get_context_data(**kwargs)
        context["submission"] = Submission.objects.get(submission_type=self.kwargs['slug'], uuid=self.kwargs['uuid'])
        return context

    def get_success_url(self):
        return reverse('submission_detail', kwargs={'slug': self.kwargs['slug'], 'uuid': self.kwargs['uuid']})


class DiscussionFlagFormView(SuccessMessageMixin, FormView):
    template_name = 'discussion/flag.html'
    form_class = DiscussionFlagForm
    model = DiscussionFlag
    success_message = 'Thanks for reporting this comment, we\'re investigating it now'

    def get_context_data(self, **kwargs):
        context = super(DiscussionFlagFormView, self).get_context_data(**kwargs)
        context["submission"] = Submission.objects.get(submission_type=self.kwargs['slug'], uuid=self.kwargs['uuid'])
        context["discussion"] = Discussion.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('submission_detail', kwargs={'slug': self.kwargs['slug'], 'uuid': self.kwargs['uuid']})

    def form_valid(self, form):
        form.instance.flagger = self.request.user
        form.instance.discussion = Discussion.objects.get(pk=self.kwargs['pk'])
        form.save()
        return super(DiscussionFlagFormView, self).form_valid(form)


class JSONFormMixin(object):
    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response


class DiscussionVoteFormBaseView(FormView):
    form_class = DiscussionVoteForm

    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response

    def form_valid(self, form):
        """
        If a user has not already voted on a discussion, create the vote.
        If a user has already voted, then the vote is deleted
        """
        discussion = get_object_or_404(Discussion, pk=form.data["discussion"])
        user = self.request.user
        vote = DiscussionVote.objects.filter(discussion=discussion, voter=user)
        already_voted = bool(len(vote) > 0)

        ret = {"success": 1}
        if not already_voted:
            v = DiscussionVote.objects.create(discussion=discussion, voter=user)
            ret['voteobj'] = v.id
        else:
            # Doesn't work this way
            vote[0].delete()
            ret["unvoted"] = 1
        return self.create_response(ret, True)

    def form_invalid(self, form):
        ret = {"success": 0, "form_errors": form.errors}
        return self.create_response(ret, False)


class DiscussionVoteFormView(JSONFormMixin, DiscussionVoteFormBaseView):
    pass
