from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc_export.actions import export_as_csv_action

from ..forms import SubjectRefusalReportForm
from ..models import SubjectRefusalReport


class SubjectRefusalReportAdmin(BaseModelAdmin):

    form = SubjectRefusalReportForm

    radio_fields = {'reason': admin.VERTICAL}
    list_filter = ('refusal_date', 'reason')

    actions = [
        export_as_csv_action(
            description="CSV Export of Subject Refusal Report",
            fields=[],
            delimiter=',',
            exclude=['user_created', 'user_modified', 'hostname_created', 'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'subject_eligibility_registered_subject__subject_identifier',
                 'gender': 'subject_eligibility_registered_subject__gender',
                 'dob': 'subject_eligibility_registered_subject__dob',
                 }),
        )]


admin.site.register(SubjectRefusalReport, SubjectRefusalReportAdmin)
