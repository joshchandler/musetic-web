from django.core.urlresolvers import reverse
from django.views.generic import FormView, DeleteView
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin

from musetic.apps.user.models import Profile, Settings
from musetic.apps.user.forms import SettingsProfileForm, SettingsGeneralForm, ChangeUsernameForm, ChangeEmailForm


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
