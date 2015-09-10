from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin


from musetic.user.models import Feedback
from musetic.user.forms import FeedbackForm


class FeedbackView(SuccessMessageMixin, CreateView):
    model = Feedback
    template_name = 'user/feedback.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('index')
    success_message = "Thank you for your feedback!"

    def form_valid(self, form):
        return super(FeedbackView, self).form_valid(form)
