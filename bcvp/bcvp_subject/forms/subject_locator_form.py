from edc_locator.forms import LocatorFormMixin

from ..models import SubjectLocator

from .base_subject_model_form import BaseSubjectModelForm


class SubjectLocatorForm(LocatorFormMixin, BaseSubjectModelForm):

    class Meta:
        model = SubjectLocator
        fields = '__all__'
