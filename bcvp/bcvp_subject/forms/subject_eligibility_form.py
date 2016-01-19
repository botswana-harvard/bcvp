from django import forms
from django.forms import ModelForm

from edc_constants.constants import DEAD, NO

from ..models import SubjectEligibility


class SubjectEligibilityForm(ModelForm):

    def clean(self):
        cleaned_data = super(SubjectEligibilityForm, self).clean()
        self.validate_omang()
        self.validate_willing_to_participate()
        return cleaned_data

    def validate_omang(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('has_omang') == NO:
            if cleaned_data.get('identity'):
                raise forms.ValidationError(
                    'You indicated that participant does not have an OMANG, you therefore CANNOT provide it.')
        else:
            if not cleaned_data.get('identity'):
                raise forms.ValidationError(
                    'You indicated that participant HAS an OMANG, please provide the OMANG number.')

    def validate_willing_to_participate(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('survival_status') == DEAD:
            if cleaned_data.get('willing_to_participate'):
                raise forms.ValidationError(
                    'You stated that participant is deceased. Please do not indicate the willingness to participate.')
        else:
            if not cleaned_data.get('willing_to_participate'):
                raise forms.ValidationError(
                    'Please indicate the participants willingnes to participate in the study.')

    class Meta:
        model = SubjectEligibility
        fields = '__all__'
