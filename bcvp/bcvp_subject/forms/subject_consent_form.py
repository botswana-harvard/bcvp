from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc_consent.forms.base_consent_form import BaseConsentForm
from edc_constants.constants import FEMALE, MALE

from bcvp.bcvp.choices import STUDY_SITES

from ..models import SubjectConsent, SubjectEligibility


class SubjectConsentForm(BaseConsentForm):

    study_site = forms.ChoiceField(
        label='Study site',
        choices=STUDY_SITES,
        initial=settings.DEFAULT_STUDY_SITE,
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):
        cleaned_data = super(SubjectConsentForm, self).clean()
        self.validate_identity()
        self.validate_omang_gender()
        self.validate_first_name()
        self.validate_last_name()
        self.validate_dob()
        return cleaned_data

    def validate_identity(self):
        cleaned_data = self.cleaned_data
        try:
            SubjectEligibility.objects.get(identity=cleaned_data.get('identity'))
        except SubjectEligibility.DoesNotExist:
            raise forms.ValidationError(
                'Identity provided does not match the identity provided in eligibility of {}. Please correct.')

    def validate_first_name(self):
        cleaned_data = self.cleaned_data
        eligibility = SubjectEligibility.objects.get(identity=cleaned_data.get('identity'))
        if cleaned_data.get('first_name') != eligibility.first_name:
            raise forms.ValidationError(
                'First name does not match first name provided in eligibility of {}. Please correct.'
                .format(eligibility.first_name))

    def validate_last_name(self):
        cleaned_data = self.cleaned_data
        eligibility = SubjectEligibility.objects.get(identity=cleaned_data.get('identity'))
        if cleaned_data.get('last_name') != eligibility.last_name:
            raise forms.ValidationError(
                'Last name does not match last name provided in eligibility of {}. Please correct.'
                .format(eligibility.last_name))

    def validate_dob(self):
        cleaned_data = self.cleaned_data
        eligibility = SubjectEligibility.objects.get(identity=cleaned_data.get('identity'))
        if cleaned_data.get('dob') != eligibility.dob:
            raise forms.ValidationError(
                'Date of birth does not match date of birth in eligibility of {}. please correct.'
                .format(eligibility.dob))

    def validate_omang_gender(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('identity')[4] == '2' and cleaned_data.get('gender') != FEMALE:
            raise forms.ValidationError(
                'Identity provided indicates participant is Female and yet gender is indicated to be Male. '
                'Please correct.')
        if cleaned_data.get('identity')[4] == '1' and cleaned_data.get('gender') != MALE:
            raise forms.ValidationError(
                'Identity provided indicates participant is Male and yet gender is indicated to be Female. '
                'Please correct.')

    class Meta:
        model = SubjectConsent
        fields = '__all__'
