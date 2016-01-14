from django.forms import ModelForm

from ..models import SubjectEligibility


class SubjectEligibilityForm(ModelForm):

    class Meta:
        model = SubjectEligibility
        fields = '__all__'
