from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms.models import ModelForm, model_to_dict, fields_for_model
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from musetic.user.models import Profile, Creator, Invite, Feedback, Settings

from registration.forms import RegistrationFormUniqueEmail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Field


class MuseticRegistrationForm(RegistrationFormUniqueEmail):
    def __init__(self, *args, **kwargs):
        super(MuseticRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Field('username', placeholder='Username'),
            Field('email', placeholder='Email'),
            Field('password1', placeholder='Password'),
            Field('password2', placeholder='Password (again)'),
            ButtonHolder(
                Submit('submit', 'Register', css_class='button')
            )
        )

    username = forms.RegexField(
        regex=r'^[\w.+-]+$',
        max_length=20,
        label=_("Username"),
        error_messages={'invalid': _("This value may contain only letters, numbers and ./+/-/_ characters.")}
    )


class MuseticAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _("Username and Password combination is incorrect. "
                           "Note that both fields are case-sensitive."),
        'inactive': _("This account is inactive."),
    }


class CreatorRequestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CreatorRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('url', placeholder='URL'),
            ButtonHolder(
                Submit('submit', 'Request Invitation', css_class='button')
            )
        )

    url = forms.URLField(label=_('Website Displaying Your Work'),
                         required=True,
                         initial='http://')

    class Meta:
        model = Creator
        exclude = ('user',)


class InviteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InviteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'invitee',
            ButtonHolder(
                Submit('submit', 'Invite', css_class='button')
            )
        )

    class Meta:
        model = Invite
        fields = ['invitee', ]

    def clean_invitee(self):
        invitee = self.cleaned_data['invitee']

        try:
            User.objects.get(email=invitee)
        except User.DoesNotExist:
            return invitee
        raise forms.ValidationError("Muser with email address {0} is already registered!".format(invitee))


class AcceptInvitationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(AcceptInvitationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Field('username', placeholder='Username'),
            Field('password1', placeholder='Password'),
            Field('password2', placeholder='Password (again)'),
            ButtonHolder(
                Submit('submit', 'Accept Invitation', css_class='button success')
            )
        )

    username = forms.RegexField(
        regex=r'^[\w.+-]+$',
        max_length=20,
        label=_("Username"),
        error_messages={'invalid': _("This value may contain only letters, numbers and ./+/-/_ characters.")}
    )
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password (again)"))

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean(self):
        """
        Verify that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['email', 'subject', 'body', ]


class SettingsProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SettingsProfileForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        _fields = ('first_name', 'last_name',)
        _initial = model_to_dict(instance.user, _fields) if instance is not None else {}
        kwargs['initial'] = _initial
        self.fields.update(fields_for_model(User, _fields))

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('settings_profile')
        self.helper.form_class = 'settings-profile-form'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'description',
            ButtonHolder(
                Submit('submit', 'Save', css_class='button success')
            )
        )

    class Meta:
        model = Profile
        exclude = ('user', 'avatar', 'creator')

    def save(self, *args, **kwargs):
        u = self.instance.user
        u.username = self.cleaned_data['username']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        return super(SettingsProfileForm, self).save(*args, **kwargs)


class ChangeUsernameForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ChangeUsernameForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            ButtonHolder(
                Submit('submit', 'Save', css_class='button success')
            )
        )

    username = forms.RegexField(
        regex=r'^[\w.+-]+$',
        max_length=20,
        label=_("Username"),
        error_messages={'invalid': _("This value may contain only letters, numbers and ./+/-/_ characters.")}
    )

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("Sorry, that username is already taken."))
        else:
            return self.cleaned_data['username']


class ChangeEmailForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('settings_email')
        self.helper.form_class = 'settings-change-email-form'
        self.helper.layout = Layout(
            'email',
            Submit('submit', 'Save', css_class='button success'),
        )

    email = forms.EmailField(label=_("Email Address"))

    def clean_email(self):
        existing = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(_("Sorry, that email address is associated with another account."))
        else:
            return self.cleaned_data['email']


class SettingsGeneralForm(forms.ModelForm):
    class Meta:
        model = Settings
        exclude = ('user', 'mail_comment_notifications')
