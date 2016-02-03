from django import forms

from edc_call_manager.models import LogEntry
from edc_constants.constants import YES
from edc_locator.forms import LocatorFormMixin

from ..models import SubjectLocator

from .base_subject_model_form import BaseSubjectModelForm


class SubjectLocatorForm(LocatorFormMixin, BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(SubjectLocatorForm, self).clean()
        self.validate_successful_contact()
        return cleaned_data

    def validate_successful_contact(self):
        cleaned_data = self.cleaned_data
        log_entries = LogEntry.objects.filter()
        flag = False
        for entry in log_entries:
            if cleaned_data.get('successful_mode_of_contact') == 'telephone':
                if entry.appt == YES:
                    flag = True
        if not flag:
            raise forms.ValidationError(
                'On the call log entry it was indicated that an appointment was not scheduled. '
                'Successful mode of contact therefore CANNOT be telephone.')

    class Meta:
        model = SubjectLocator
        fields = '__all__'
