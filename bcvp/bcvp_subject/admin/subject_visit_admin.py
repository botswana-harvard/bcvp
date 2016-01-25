from django.contrib import admin
from copy import copy

from edc_base.modeladmin.admin import BaseModelAdmin
from edc_visit_tracking.admin import VisitAdminMixin

from bcvp.bcvp_lab.models import SubjectRequisition

from ..forms import SubjectVisitForm
from ..models import SubjectVisit


class SubjectVisitAdmin(VisitAdminMixin, BaseModelAdmin):

    form = SubjectVisitForm
    visit_attr = 'subject_visit'
    requisition_model = SubjectRequisition
    dashboard_type = 'subject'

    def get_fieldsets(self, request, obj=None):
        fields = copy(self.fields)
        fields.remove('information_provider')
        fields.remove('information_provider_other')
        return [(None, {'fields': fields})]

admin.site.register(SubjectVisit, SubjectVisitAdmin)
