from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc_base.form.forms import BaseModelForm
from edc_constants.constants import ON_STUDY
from edc_visit_tracking.forms import VisitFormMixin

from bcvp.bcvp.choices import VISIT_REASON, VISIT_INFO_SOURCE, VISIT_STUDY_STATUS

from ..models import SubjectVisit


class SubjectVisitForm (VisitFormMixin, BaseModelForm):

    participant_label = 'subject'

    study_status = forms.ChoiceField(
        label='What is the subject\'s current study status',
        choices=VISIT_STUDY_STATUS,
        initial=ON_STUDY,
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    reason = forms.ChoiceField(
        label='Reason for visit',
        choices=[choice for choice in VISIT_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    info_source = forms.ChoiceField(
        label='Source of information',
        required=False,
        choices=[choice for choice in VISIT_INFO_SOURCE],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    class Meta:
        model = SubjectVisit
        fields = '__all__'
