from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc_consent.forms.base_consent_form import BaseConsentForm
from edc_constants.constants import OMANG

from bcvp.bcvp.choices import STUDY_SITES

from ..models import SubjectConsent


class SubjectConsentForm(BaseConsentForm):

    study_site = forms.ChoiceField(
        label='Study site',
        choices=STUDY_SITES,
        initial=settings.DEFAULT_STUDY_SITE,
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):
        cleaned_data = super(SubjectConsentForm, self).clean()
        if cleaned_data.get('identity_type') == OMANG and cleaned_data.get('identity')[4] in ['12']:
            raise forms.ValidationError('Identity provided indicates participant is Male. Please correct.')
        return cleaned_data

    class Meta:
        model = SubjectConsent
        fields = '__all__'
