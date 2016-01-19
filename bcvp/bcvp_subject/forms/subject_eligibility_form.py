from django import forms
from django.forms import ModelForm

from edc_constants.constants import DEAD, NO, FEMALE, MALE

from ..models import SubjectEligibility


class SubjectEligibilityForm(ModelForm):

    def clean(self):
        cleaned_data = super(SubjectEligibilityForm, self).clean()
        self.validate_omang_gender()
        self.validate_willing_to_participate()
        SubjectEligibility(**cleaned_data).get_recent_infection_or_raise(forms.ValidationError)
        return cleaned_data

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
