from ..models import SexualBehaviour

from .base_subject_model_form import BaseSubjectModelForm


class SexualBehaviourForm(BaseSubjectModelForm):

    class Meta:
        model = SexualBehaviour
        fields = '__all__'
