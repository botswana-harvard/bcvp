from django import forms

from edc_constants.constants import POS

from ..models import RecentPartner

from .base_subject_model_form import BaseSubjectModelForm


class RecentPartnerForm(BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(RecentPartnerForm, self).clean()
        self.validate_recent_sex()
        self.validate_first_sex()
        self.validate_partner_status()
        return cleaned_data

    def validate_recent_sex(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('last_sex_contact'):
            if not cleaned_data.get('last_sex_period'):
                raise forms.ValidationError(
                    'Please indicate whether the last sex period is in days, months or years.')
        if not cleaned_data.get('last_sex_contact'):
            if cleaned_data.get('last_sex_period'):
                raise forms.ValidationError(
                    'Please do not provide the period that has past since the last sex as it is indicated to be 0.')

    def validate_first_sex(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('first_sex_contact') > 0:
            if not cleaned_data.get('first_sex_period'):
                raise forms.ValidationError(
                    'Please indicate whether the first sex period is in days, months or years.')
        if not cleaned_data.get('first_sex_contact'):
            if cleaned_data.get('first_sex_period'):
                raise forms.ValidationError(
                    'Please do not provide the period that has past since the first sex with this person as it is '
                    'indicated to be 0.')

    def validate_partner_status(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('partner_status') != POS:
            if cleaned_data.get('partner_arv'):
                raise forms.ValidationError(
                    'You indicated partner is {}, question on whether he/she is taking antiretrovirals '
                    'should be None'.format(cleaned_data.get('partner_status')))
        else:
            if not cleaned_data.get('partner_arv'):
                raise forms.ValidationError(
                    'You indicated partner is Positive. Please indicate whether they are on ARV.')

    class Meta:
        model = RecentPartner
        fields = '__all__'
