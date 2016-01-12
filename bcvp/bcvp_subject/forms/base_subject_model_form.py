from edc_base.form.forms import BaseModelForm

from ..models import SubjectVisit


class BaseSubjectModelForm(BaseModelForm):

    visit_model = SubjectVisit
