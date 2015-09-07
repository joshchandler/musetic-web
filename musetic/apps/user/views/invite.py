from django.contrib.sites.models import RequestSite
from django.shortcuts import redirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from musetic.apps.user.models import Invite
from musetic.apps.user.forms import InviteForm, AcceptInvitationForm
from musetic.apps.user import signals

from registration.views import _RequestPassingFormView
from braces.views import AnonymousRequiredMixin


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
