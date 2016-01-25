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
        self.validate_on_arv()
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
                    'You have indicated that HIV related medical or clinical care was received. Please DO NOT '
                    'provide a reason why medical care was not received')

    def validate_ever_taken_arv(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('ever_taken_arv') == NO:
            if not cleaned_data.get('why_no_arv'):
                self._errors["why_no_arv"] = ErrorList(["This field is required."])
                raise forms.ValidationError('You have indicated that ARVs were NOT taken. Please provide a reason why')
            if cleaned_data.get('first_arv'):
                self._errors["first_arv"] = ErrorList(["This field should not be filled"])
                raise forms.ValidationError('You have indicated that ARVs were never taken. You cannot provide '
                                            'a start date')
        if cleaned_data.get('ever_taken_arv') == YES:
            if cleaned_data.get('why_no_arv'):
                self._errors["why_no_arv"] = ErrorList(["This field should not be filled"])
                raise forms.ValidationError(
                    'You have indicated that ARVs were taken. You CANNOT provide a reason why ARVs were not taken.')
            if not cleaned_data.get('first_arv'):
                self._errors["first_arv"] = ErrorList(["This field is required."])
                raise forms.ValidationError('You have indicated that ARVs were taken. Please indicate ARV start date.')

    def validate_on_arv(self):
        cleaned_data = self.cleaned_data()
        if cleaned_data.get('on_arv') == YES:
            if not cleaned_data.get('arv_evidence'):
                self._errors["arv_evidence"] = ErrorList(["This field cannot be None"])
                raise forms.ValidationError(
                    'You have indicated participant is currently on ARV. Please indicate if there is evidence.')
            if not cleaned_data.get('clinic_receiving_from'):
                self._errors["clinic_receiving_from"] = ErrorList(["This field cannot be None"])
                raise forms.ValidationError(
                    'You have indicated participant is currently on ARV. Please indicate where they receive therapy.')
        if cleaned_data.get('on_arv') == NO:
            if cleaned_data.get('arv_evidence'):
                self._errors["arv_evidence"] = ErrorList(["This field should not be filled."])
                raise forms.ValidationError(
                    'If patient is not on ARV, do not indicate whether there is evidence participant is on therapy.')
            if cleaned_data.get('clinic_receiving_from'):
                self._errors["clinic_receiving_from"] = ErrorList(["This field should not be filled."])
                raise forms.ValidationError(
                    'If patient is not on ARV, do not indicate where therapy is received from.')

    class Meta:
        model = HivCareAdherence
        fields = '__all__'
