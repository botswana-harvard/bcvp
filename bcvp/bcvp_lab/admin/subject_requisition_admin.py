from copy import copy

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from lab_requisition.admin import RequisitionAdminMixin

from bcvp.bcvp_subject.models import SubjectVisit

from ..forms import SubjectRequisitionForm
from ..models import SubjectRequisition, Panel


class SubjectRequisitionAdmin(RequisitionAdminMixin, BaseModelAdmin):

    dashboard_type = 'subject'
    form = SubjectRequisitionForm
    label_template_name = 'requisition_label'
    visit_attr = 'subject_visit'
    visit_model = SubjectVisit
    panel_model = Panel

    def get_fieldsets(self, request, obj=None):
        fields = copy(self.fields)
        panel_names = [
            'Vaginal swab (Storage)',
            'Rectal swab (Storage)',
            'Skin Swab (Storage)',
            'Vaginal Swab (multiplex PCR)']
        panel = self.panel_model.objects.get(id=request.GET.get('panel'))
        if panel.name in panel_names:
            try:
                fields.remove(fields.index('estimated_volume'))
            except ValueError:
                pass
        try:
            fields.remove(fields.index('test_code'))
        except ValueError:
            pass
        return [(None, {'fields': self.fields})]

admin.site.register(SubjectRequisition, SubjectRequisitionAdmin)
