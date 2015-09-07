from django.core.urlresolvers import reverse
from django.views.generic import UpdateView
from django.http import Http404
from django.contrib.auth.models import User


from musetic.apps.user.models import Settings
from musetic.apps.user.forms import SettingsForm


class UserSettingsView(UpdateView):
    model = Settings
    template_name = 'user/settings.html'
    form_class = SettingsForm
    slug_field = 'user__username'
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        """
        The edit profile page is not visible unless the user is activated
        """
        user = User.objects.get(username=self.kwargs['username'])
        if request.user.username == self.kwargs['username']:
            if user.is_active:
                return super(UserSettingsView, self).dispatch(request, *args, **kwargs)
        raise Http404

    def get_success_url(self):
        return reverse('user_profile', kwargs={'username': self.kwargs['username']})
