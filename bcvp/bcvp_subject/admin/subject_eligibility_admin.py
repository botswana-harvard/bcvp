from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc_export.actions import export_as_csv_action

from ..forms import SubjectEligibilityForm
from ..models import SubjectEligibility


class SubjectEligibilityAdmin(BaseModelAdmin):

    form = SubjectEligibilityForm

    fields = ('eligibility_id',
              'report_datetime',
              'age_in_years',
              'has_omang',
              'survival_status',
              'willing_to_participate')
    radio_fields = {
        'has_omang': admin.VERTICAL,
        'survival_status': admin.VERTICAL,
        'willing_to_participate': admin.VERTICAL,
    }

    readonly_fields = ('eligibility_id',)
    list_display = ('report_datetime', 'age_in_years', 'is_eligible', 'is_consented')
    list_filter = ('report_datetime', 'is_eligible', 'is_consented')

    actions = [
        export_as_csv_action(
            description="CSV Export of Subject Eligibility",
            fields=[],
            delimiter=',',
            exclude=['user_created', 'user_modified', 'hostname_created', 'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'registered_subject__subject_identifier',
                 'gender': 'registered_subject__gender',
                 'dob': 'registered_subject__dob',
                 }),
        )]

admin.site.register(SubjectEligibility, SubjectEligibilityAdmin)
