from django import forms

from ..models import ResidencyMobility

from .base_subject_model_form import BaseSubjectModelForm
from edc_constants.constants import NOT_APPLICABLE


class ResidencyMobilityForm(BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(ResidencyMobilityForm, self).clean()
        self.validate_permanent_resident()
        self.validate_cattle_postlands()
        return cleaned_data

    def validate_permanent_resident(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('permanent_resident') == 'Yes':
            if cleaned_data.get('nights_away') == 'more than 6 months':
                raise forms.ValidationError(
                    'If participant has spent 14 or more nights per month in this community, nights away CANNOT be '
                    'more than 6months.')

    def validate_cattle_postlands(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('cattle_postlands') == 'Other community':
            if not cleaned_data.get('cattle_postlands_other'):
                raise forms.ValidationError('If participant was staying in another community, specify the community.')
        if cleaned_data.get('cattle_postlands') != NOT_APPLICABLE:
            if cleaned_data.get('nights_away') == 'zero':
                raise forms.ValidationError(
                    'If participant spent zero nights away, times spent away should be Not applicable.')
        if cleaned_data.get('cattle_postlands') == NOT_APPLICABLE:
            if cleaned_data.get('nights_away') != 'zero':
                raise forms.ValidationError(
                    'Participant has spent more than zero nights away, times spent away CANNOT be Not applicable.')

    class Meta:
        model = ResidencyMobility
        fields = '__all__'
