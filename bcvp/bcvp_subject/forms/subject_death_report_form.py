from edc_death_report.forms import DeathReportFormMixin

from ..models import SubjectDeathReport

from .base_subject_model_form import BaseSubjectModelForm


class SubjectDeathReportForm(DeathReportFormMixin, BaseSubjectModelForm):

    class Meta:
        model = SubjectDeathReport
        fields = '__all__'
