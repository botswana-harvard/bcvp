from ..models import RecentPartner

from .base_subject_model_form import BaseSubjectModelForm


class RecentPartnerForm(BaseSubjectModelForm):

    class Meta:
        model = RecentPartner
        fields = '__all__'
