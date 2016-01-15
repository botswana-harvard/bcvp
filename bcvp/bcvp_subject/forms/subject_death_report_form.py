from django.forms import ModelForm

from edc_death_report.forms import DeathReportFormMixin

from ..models import SubjectDeathReport


class SubjectDeathReportForm(ModelForm):

    class Meta:
        model = SubjectDeathReport
        fields = '__all__'
