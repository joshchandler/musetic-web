from django.conf import settings
from django.views.generic.base import TemplateResponse
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.sites.shortcuts import get_current_site

from musetic.apps.user.forms import MuseticRegistrationForm, MuseticAuthenticationForm

from registration.backends.default.views import ActivationView, RegistrationView
from braces.views import AnonymousRequiredMixin


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
