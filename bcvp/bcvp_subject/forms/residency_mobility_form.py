from ..models import ResidencyMobility

from .base_subject_model_form import BaseSubjectModelForm


class ResidencyMobilityForm(BaseSubjectModelForm):

    class Meta:
        model = ResidencyMobility
        fields = '__all__'
