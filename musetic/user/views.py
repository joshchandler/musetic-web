from django.conf import settings
from django.db import models
from django.http import Http404
from django.views.generic import DetailView, CreateView, FormView, DeleteView
from django.views.generic.base import TemplateResponse, TemplateView
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import REDIRECT_FIELD_NAME, login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import RequestSite

from .forms import (
    MuseticRegistrationForm, MuseticAuthenticationForm, CreatorRequestForm,
    InviteForm, AcceptInvitationForm, FeedbackForm, SettingsProfileForm,
    ChangeUsernameForm, ChangeEmailForm, SettingsGeneralForm
)
from .models import User, Profile, Creator, Invite, Feedback, Settings
from musetic.user import signals

from musetic.submission.models import Submission, Vote

from registration.backends.default.views import ActivationView, RegistrationView
from braces.views import AnonymousRequiredMixin

from registration.views import _RequestPassingFormView


class RegistrationViewUniqueEmail(AnonymousRequiredMixin, RegistrationView):
    """
    Already logged in users can't view the registration page via AnonymousRequiredMixin
    Email must be unique
    """
    form_class = MuseticRegistrationForm

    def get_context_data(self, **kwargs):
        context = super(RegistrationViewUniqueEmail, self).get_context_data(**kwargs)
        context['musetic_registration_form'] = MuseticRegistrationForm()
        return context


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=MuseticAuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


class ActivationRedirect(ActivationView):
    def get_success_url(self, request, user):
        return 'index', (), {}


@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('settings_password_change')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


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
            Submission.objects.all().annotate(
                votes=models.Count('submission_votes')
            ).select_related().filter(
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
            Submission.objects.all().annotate(
                votes=models.Count('submission_votes')
            ).select_related().filter(
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


class InviteFormView(_RequestPassingFormView):
    model = Invite
    template_name = 'user/invite.html'
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    form_class = InviteForm

    def form_valid(self, request, form):
        invitation = self.invite(request, **form.cleaned_data)
        success_url = self.get_success_url(request, invitation)

        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(success_url)

    def invite(self, request, **cleaned_data):
        invitee = cleaned_data['invitee']
        site = RequestSite(request)
        invitation = Invite.objects.create_invitation(self.request.user, invitee, site, request=request)

        signals.invitation_sent.send(
            sender=self.__class__,
            invitation=invitation,
            request=request
        )
        return invitation

    def get_context_data(self, **kwargs):
        context = super(InviteFormView, self).get_context_data(**kwargs)
        context["sent_invites"] = Invite.objects.filter(inviter=self.request.user, accepted=False)
        accepted_invites = Invite.objects.filter(inviter=self.request.user, accepted=True)
        context["accepted_invites"] = accepted_invites
        context["accepted_users"] = context["accepted_invites"]
        return context

    def get_success_url(self, request, user):
        """
        Return the name of the URL to redirect to after a
        successful creator request
        """
        return 'user_invite'


class AcceptInvitationView(AnonymousRequiredMixin, _RequestPassingFormView):
    model = User
    template_name = 'user/invite_accept.html'
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    form_class = AcceptInvitationForm

    def dispatch(self, request, *args, **kwargs):
        if Invite.objects.get(activation_key=self.kwargs['activation_key']):
            invite = Invite.objects.get(activation_key=self.kwargs['activation_key'])
            if invite.accepted is False:
                return super(AcceptInvitationView, self).dispatch(request, *args, **kwargs)
        raise Http404

    def form_valid(self, request, form):
        accept = self.accept(request, **form.cleaned_data)
        new_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password2'])
        login(request, new_user)
        success_url = self.get_success_url(request, accept)

        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(success_url)

    def accept(self, request, **cleaned_data):

        invite = Invite.objects.get(activation_key=self.kwargs['activation_key'])

        username = cleaned_data['username']
        password = cleaned_data['password2']

        site = RequestSite(request)
        send_email = True

        # Change the invite to accepted
        invite.accepted = True
        invite.save()

        accepted_invitation = Invite.objects.accept_invitation(
            invite, username, invite.invitee,
            password, site, send_email, request=request
        )

        signals.invitation_accepted.send(
            sender=self.__class__,
            invitation=accepted_invitation,
            request=request
        )

        return accepted_invitation

    def get_context_data(self, **kwargs):
        context = super(AcceptInvitationView, self).get_context_data(**kwargs)
        context["invite"] = Invite.objects.get(activation_key=self.kwargs['activation_key'])

        context["accept_invitation_form"] = AcceptInvitationForm()
        return context

    def get_success_url(self, request, user):
        return 'index', (), {}


    
class FeedbackView(SuccessMessageMixin, CreateView):
    model = Feedback
    template_name = 'user/feedback.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('index')
    success_message = "Thank you for your feedback!"

    def form_valid(self, form):
        return super(FeedbackView, self).form_valid(form)


class SettingsProfile(SuccessMessageMixin, FormView):
    model = Profile
    form_class = SettingsProfileForm
    template_name = 'user/settings_profile.html'
    success_message = 'You have successfully updated your profile'

    def dispatch(self, request, *args, **kwargs):
        """
        The edit profile page is not visible unless the user is activated
        """
        user = User.objects.get(username=self.request.user.username)
        if user.is_active:
            return super(SettingsProfile, self).dispatch(request, *args, **kwargs)
        raise Http404

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user.username)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.profile.description = form.cleaned_data['description']
        user.save()
        user.profile.save()
        return super(SettingsProfile, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SettingsProfile, self).get_context_data(**kwargs)
        context["settings_profile_form"] = SettingsProfileForm()
        return context

    def get_success_url(self):
        return reverse('settings_profile')


class SettingsChangeUsername(FormView):
    model = User
    template_name = 'user/settings_username.html'
    form_class = ChangeUsernameForm

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user.username)
        user.username = form.cleaned_data['username']
        user.save()
        return super(SettingsChangeUsername, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SettingsChangeUsername, self).get_context_data(**kwargs)
        context["change_username_form"] = ChangeUsernameForm()
        return context

    def get_success_url(self):
        return reverse('settings_username')


class SettingsChangeEmail(FormView):
    model = User
    template_name = 'user/settings_email.html'
    form_class = ChangeEmailForm

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user.username)
        user.email = form.cleaned_data['email']
        user.save()
        return super(SettingsChangeEmail, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SettingsChangeEmail, self).get_context_data(**kwargs)
        context['change_email_form'] = ChangeEmailForm()
        return context

    def get_success_url(self):
        return reverse('settings_email')


class SettingsDeleteAccount(DeleteView):
    model = User
    template_name = 'user/settings_delete.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    success_url = '/'


class SettingsGeneral(FormView):
    model = Settings
    template_name = 'user/settings_general.html'
    form_class = SettingsGeneralForm

    def dispatch(self, request, *args, **kwargs):
        """
        The edit profile page is not visible unless the user is activated
        """
        user = User.objects.get(username=self.request.user)
        if user.is_active:
            return super(SettingsGeneral, self).dispatch(request, *args, **kwargs)
        raise Http404

    def form_valid(self, form):
        settings = Settings.objects.get(user=self.request.user)
        settings.show_feedback_tab = form.cleaned_data['show_feedback_tab']
        settings.save()
        return super(SettingsGeneral, self).form_valid(form)

    def get_success_url(self):
        return reverse('settings_general')
