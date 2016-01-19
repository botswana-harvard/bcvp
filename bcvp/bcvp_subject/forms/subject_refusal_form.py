from django import forms
from django.forms import ModelForm

from ..models import SubjectRefusal


class SubjectRefusalForm(ModelForm):

    def clean(self):
        cleaned_data = super(SubjectRefusalForm, self).clean()
        self.validate_required()
        return cleaned_data

    def validate_required(self):
        cleaned_data = self.cleaned_data
        if self.instance.pk:
            if not cleaned_data.get('refusal_date'):
                raise forms.ValidationError(
                    '{} is required. Please fill it in.'.format('Refusal Date'))
            if not cleaned_data.get('reason'):
                raise forms.ValidationError(
                    '{} is required. Please fill it in.'.format('Reason'))

    class Meta:
        model = SubjectRefusal
        fields = '__all__'
