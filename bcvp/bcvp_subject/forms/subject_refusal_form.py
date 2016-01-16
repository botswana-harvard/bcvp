from django.forms import ModelForm

from ..models import SubjectRefusal


class SubjectRefusalForm(ModelForm):

    class Meta:
        model = SubjectRefusal
        fields = '__all__'
