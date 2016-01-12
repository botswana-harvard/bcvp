from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from bcvp.bcvp.choices import OFF_STUDY_REASON

from ..models import SubjectOffStudy, SubjectConsent

from .base_subject_model_form import BaseSubjectModelForm


class SubjectOffStudyForm (BaseSubjectModelForm):

    reason = forms.ChoiceField(
        label='Please code the primary reason participant taken off-study',
        choices=[choice for choice in OFF_STUDY_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):
        cleaned_data = super(SubjectOffStudyForm, self).clean()
        self.validate_offstudy_date()
        return cleaned_data

    def validate_offstudy_date(self):
        cleaned_data = self.cleaned_data
        try:
            subject_identifier = cleaned_data.get(
                'subject_visit').appointment.registered_subject.subject_identifier
            subject_consent = SubjectConsent.objects.get(
                registered_subject__subject_identifier=subject_identifier)
            try:
                if cleaned_data.get('offstudy_date') < subject_consent.consent_datetime.date():
                    raise forms.ValidationError("Off study date cannot be before consent date")
                if cleaned_data.get('offstudy_date') < subject_consent.dob:
                    raise forms.ValidationError("Off study date cannot be before dob")
            except AttributeError:
                pass
        except SubjectConsent.DoesNotExist:
            raise forms.ValidationError('Subject Consent does not exist.')

    class Meta:
        model = SubjectOffStudy
