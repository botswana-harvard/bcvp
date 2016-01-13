from ..models import HivCareAdherence

from .base_subject_model_form import BaseSubjectModelForm


class HivCareAdherenceForm(BaseSubjectModelForm):

    class Meta:
        model = HivCareAdherence
        fields = '__all__'
