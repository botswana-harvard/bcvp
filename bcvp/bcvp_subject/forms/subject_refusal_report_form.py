from django.forms import ModelForm

from ..models import SubjectRefusalReport


class SubjectRefusalReportForm(ModelForm):

    class Meta:
        model = SubjectRefusalReport
        fields = '__all__'
