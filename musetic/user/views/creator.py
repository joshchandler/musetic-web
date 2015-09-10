from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import TemplateView
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite

from musetic.user.models import Creator
from musetic.user.forms import CreatorRequestForm
from musetic.user import signals

from registration.views import _RequestPassingFormView


class CreatorRequestView(_RequestPassingFormView):
    """
    The FormView Class for Creator Requests.

    This subclasses from django-registration-redux class _RequestPassingFormView
    enabling finer-grained processing of HTTP requests.
    """
    model = Creator
    form_class = CreatorRequestForm
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    template_name = 'user/creator_request_form.html'

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        try:
            new_creator = user.creator
        except ObjectDoesNotExist:
            new_creator = None
        if new_creator is None:
            return super(CreatorRequestView, self).dispatch(request, *args, **kwargs)
        return redirect('creator_request_sent')

    def form_valid(self, request, form):
        new_creator = self.creator_request(request, **form.cleaned_data)
        success_url = self.get_success_url(request, new_creator)

        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(success_url)

    def get_context_data(self, **kwargs):
        context = super(CreatorRequestView, self).get_context_data(**kwargs)
        context["creator_request_form"] = CreatorRequestForm()
        return context

    def creator_request(self, request, **cleaned_data):
        """
        Given a user provides a url, a new entry of the
        `musetic.apps.user.UserCreator` model will be created, tied
        to the `User`

        An email is to be sent to join@musetic.com
        """
        user = self.request.user
        url = cleaned_data['url']
        site = RequestSite(request)
        new_creator = Creator.objects.create_inactive_creator(
            user, url, site,
            send_email=True,
            request=request,
        )
        signals.creator_registered.send(sender=self.__class__,
                                        creator=new_creator,
                                        request=request)

        return new_creator

    def get_success_url(self, request, user):
        """
        Return the name of the URL to redirect to after a
        successful creator request
        """
        return 'creator_request_sent', (), {}


class CreatorRequestSentView(TemplateView):
    """
    The View musers see after successfully requesting an invite
    """
    template_name = 'user/creator_request_sent.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        try:
            new_creator = user.creator
        except ObjectDoesNotExist:
            new_creator = False
        if new_creator is False:
            return redirect('creator_request')
        return super(CreatorRequestSentView, self).dispatch(request, *args, **kwargs)


class CreatorAcceptView(TemplateView):
    """
    This view turns a Muser's Creator account to True

    This is only accessible to admins of the site.
    """
    http_method_names = ['get']
    template_name = 'user/creator_accept.html'
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        creator = Creator.objects.get(user__username=self.kwargs['username'])
        if user.is_staff:
            success_url = self.get_success_url(request, creator)
            if not creator.is_creator:
                return super(CreatorAcceptView, self).dispatch(request, *args, **kwargs)
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        raise Http404

    def get(self, request, *args, **kwargs):
        accepted_creator = self.creator_accept(request, *args, **kwargs)
        if accepted_creator:
            success_url = self.get_success_url(request, accepted_creator)
            try:
                to, args, kwargs = success_url
                return redirect(to, *args, **kwargs)
            except ValueError:
                return redirect(success_url)
        return super(CreatorAcceptView, self).get(request, *args, **kwargs)

    def creator_accept(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        site = RequestSite(request)
        accepted_creator = Creator.objects.activate_creator(
            user, site,
            send_email=True,
            request=request,
        )
        if accepted_creator:
            signals.creator_accepted.send(sender=self.__class__,
                                          creator=accepted_creator,
                                          request=request)

        return accepted_creator

    def get_context_data(self, **kwargs):
        context = super(CreatorAcceptView, self).get_context_data(**kwargs)
        context["creator"] = User.objects.get(username=self.kwargs['username'])
        return context

    def get_success_url(self, request, user):
        return 'creator_activated', (), {'username': self.kwargs['username']}


class CreatorActivatedView(TemplateView):
    template_name = 'user/creator_activated.html'
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        creator = Creator.objects.get(user__username=self.kwargs['username'])
        if user.is_staff:
            if creator.is_creator:
                return super(CreatorActivatedView, self).dispatch(request, *args, **kwargs)
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(CreatorActivatedView, self).get_context_data(**kwargs)
        context["creator"] = User.objects.get(username=self.kwargs['username'])
        return context
