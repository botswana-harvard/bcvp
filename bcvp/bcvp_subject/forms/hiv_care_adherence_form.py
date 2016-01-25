from django import forms
from django.forms.util import ErrorList

from edc_constants.constants import NO, YES

from ..models import HivCareAdherence

from .base_subject_model_form import BaseSubjectModelForm


class HivCareAdherenceForm(BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(HivCareAdherenceForm, self).clean()
        self.validate_first_positive()
        self.validate_no_medical_care()
        self.validate_ever_taken_arv()
        return cleaned_data

    def validate_first_positive(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('first_positive'):
            if not cleaned_data.get('medical_care'):
                self._errors["medical_care"] = ErrorList(["This field is required."])
                raise forms.ValidationError(
                    'First HIV result was provided please answer question on whether HIV related medical '
                    'or clinical care.')
            if not cleaned_data.get('ever_recommended_arv'):
                self._errors["ever_recommended_arv"] = ErrorList(["This field is required."])
                raise forms.ValidationError(
                    'First HIV result was provided please answer question on recommendation to start '
                    'ARV by healthworker.')

    def validate_no_medical_care(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('medical_care') == NO:
            if not cleaned_data.get('no_medical_care'):
                self._errors["no_medical_care"] = ErrorList([
                    "This field is required. Medical or clinical care was received"])
                raise forms.ValidationError(
                    'You have indicated that NO HIV related medical or clinical care was taken. '
                    'Please provide a reason.')
        if cleaned_data.get('medical_care') == YES:
            if cleaned_data.get('no_medical_care'):
                self._errors["no_medical_care"] = ErrorList([
                    "Don't answer this question. Medical or clinical care was not received"])
                raise forms.ValidationError(
                    'You have indicated that HIV related medical or clinical care was recieved. Please DO NOT '
                    'provide a reason why medical care was not received')

    def validate_ever_taken_arv(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('ever_taken_arv') == NO:
            if not cleaned_data.get('why_no_arv'):
                self._errors["why_no_arv"] = ErrorList(["This field is required."])
                raise forms.ValidationError('You have indicated that ARVs were NOT taken. Please provide a reason why')
        if cleaned_data.get('ever_taken_arv') == YES:
            if cleaned_data.get('why_no_arv'):
                self._errors["why_no_arv"] = ErrorList(["This field should not be filled"])
                raise forms.ValidationError(
                    'You have indicated that ARVs were taken. You CANNOT provide a reason why ARVs were not taken.')

    class Meta:
        model = HivCareAdherence
        fields = '__all__'
