from django.forms.models import ModelForm

from .models import Discussion, DiscussionVote, DiscussionFlag

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit


class DiscussionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DiscussionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            'comment',
            ButtonHolder(
                Submit('submit', 'Comment', css_class='button')
            )
        )

    class Meta:
        model = Discussion
        fields = ['comment', ]


class DiscussionEditForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DiscussionEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'comment',
            ButtonHolder(
                Submit('submit', 'Save', css_class='button')
            )
        )

    class Meta:
        model = Discussion
        fields = ['comment', ]


class DiscussionVoteForm(ModelForm):
    class Meta:
        model = DiscussionVote
        exclude = ()


class DiscussionFlagForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DiscussionFlagForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'discussion-flag-form'
        self.helper.layout = Layout(
            'reason',
        )

    class Meta:
        model = DiscussionFlag
        fields = ['reason', ]
