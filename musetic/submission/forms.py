import os

from django import forms
from django.forms.models import ModelForm
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from .models import Submission, Vote, Flag
from .conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit


class SubmissionForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(SubmissionForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.form_action = '.'
    #     self.helper.layout = Layout(
    #         Field('submission_type', id='selection'),
    #         'title',
    #         'description',
    #         'thumbnail',
    #         'url',
    #         ButtonHolder(
    #             Submit('submit', 'Submit', css_class='button')
    #         ),
    #         Field('next', type='hidden'),
    #     )
    #
    # submission_type = forms.ChoiceField(label='Project Type',
    #                                     choices=[(media.value, media.name) for media in MediaTypes])
    # title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))

    class Meta:
        model = Submission
        fields = ['submission_type', 'title', 'description', 'thumbnail', 'url', ]

    def clean_thumbnail(self):
        data = self.cleaned_data['thumbnail']

        if data is not None:
            if settings.SUBMISSION_ALLOWED_FILE_EXTS:
                root, ext = os.path.splitext(data.name.lower())
                if ext not in settings.SUBMISSION_ALLOWED_FILE_EXTS:
                    valid_exts = ", ".join(settings.SUBMISSION_ALLOWED_FILE_EXTS)
                    error = _("%(ext)s is an invalid file extension. "
                              "Authorized extensions are : %(valid_exts_list)s")
                    raise forms.ValidationError(error %
                                                {'ext': ext,
                                                 'valid_exts_list': valid_exts})
            if data.size > settings.SUBMISSION_MAX_SIZE:
                error = _("Your file is too big (%(size)s), "
                          "the maximum allowed size is %(max_valid_size)s")
                raise forms.ValidationError(error % {
                    'size': filesizeformat(data.size),
                    'max_valid_size': filesizeformat(settings.SUBMISSION_MAX_SIZE)
                })

        return data


class SubmissionEditForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubmissionEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'submission_type',
            'title',
            'description',
            'url',
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button')
            )
        )

    class Meta:
        model = Submission
        fields = ['submission_type', 'title', 'description', 'url', ]


class SubmissionEditThumbnailForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubmissionEditThumbnailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            'thumbnail',
            Submit('submit', 'Change Thumbnail', css_class='button')
        )

    class Meta:
        model = Submission
        fields = ['thumbnail', ]


class VoteForm(ModelForm):
    class Meta:
        model = Vote


class FlagForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FlagForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'flag-form'
        self.helper.layout = Layout(
            'reason',
        )

    reason = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Flag
        fields = ['reason', ]
