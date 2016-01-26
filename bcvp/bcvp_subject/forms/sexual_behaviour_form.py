from django import forms
from django.forms.util import ErrorList

from edc_constants.constants import YES, NO

from ..models import SexualBehaviour

from .base_subject_model_form import BaseSubjectModelForm


class SexualBehaviourForm(BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(SexualBehaviourForm, self).clean()
        self.validate_ever_sex()
        self.validate_more_sex()
        self.validate_partner_numbers()
        return cleaned_data

    def validate_ever_sex(self):
        """Ensuring that the number of last year partners is not greater than lifetime partners"""
        cleaned_data = self.cleaned_data
        if cleaned_data.get('ever_sex') == YES:
            if not cleaned_data.get('lifetime_sex_partners'):
                raise forms.ValidationError('If participant has ever had sex, CANNOT have 0 lifetime partners.')
            if not cleaned_data.get('condom'):
                raise forms.ValidationError(
                    'If participant has had sex at some point in their life, did participant '
                    'use a condom the last time he/she had sex?')
            if not cleaned_data.get('alcohol_sex'):
                raise forms.ValidationError(
                    'If participant has had sex at some point in their life, did participant '
                    'drink alcohol before sex last time?')
        if cleaned_data.get('ever_sex') == NO:
            if cleaned_data.get('lifetime_sex_partners') > 0:
                self._errors["lifetime_sex_partners"] = ErrorList(["This field should not be 0"])
                raise forms.ValidationError(
                    'If participant has never had sex, CANNOT have sex partners be greater than 0.')
            if cleaned_data.get('condom'):
                self._errors["condom"] = ErrorList(["This field should not be None"])
                raise forms.ValidationError(
                    'Participant has indicated they have never had sex, therefore question on condom use during '
                    'sex is not applicable and should be None')
            if cleaned_data.get('alcohol_sex'):
                self._errors["alcohol_sex"] = ErrorList(["This field should not be None"])
                raise forms.ValidationError(
                    'Participant has indicated they have never had sex, therefore question on drinking alcohol '
                    'during sex is not applicable.')

    def validate_more_sex(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('more_sex') == YES:
            if not cleaned_data.get('last_year_partners'):
                raise forms.ValidationError(
                    'If participant has had sex with somebody living outside of the community in the past year, '
                    'CANNOT have 0 last year partners.')
        if cleaned_data.get('more_sex') == NO:
            if cleaned_data.get('last_year_partners') > 0:
                raise forms.ValidationError(
                    'Participant is indicated to have had sex in the past year with someone outside of the community.'
                    'Please provide the number of sex partners in the past year.')
        if not cleaned_data.get('more_sex'):
            if cleaned_data.get('last_year_partners') > 0:
                raise forms.ValidationError(
                    'If participant has had sex with anyone in the past 12months, has participant '
                    'had sex with anyone outside community in the past 12months?')

    def validate_partner_numbers(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('last_year_partners') > cleaned_data.get('lifetime_sex_partners'):
            raise forms.ValidationError(
                'Number of partners in the past 12months CANNOT exceed number of life time partners.')

    class Meta:
        model = SexualBehaviour
        fields = '__all__'
