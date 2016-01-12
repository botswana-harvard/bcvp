from collections import OrderedDict

from edc_export.actions import export_as_csv_action
from edc_base.modeladmin.admin import BaseModelAdmin

from ..models import SubjectVisit


class BaseSubjectModelAdmin(BaseModelAdmin):

    dashboard_type = 'subject'
    visit_model_name = 'subjectvisit'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject_visit":
            if request.GET.get('subject_visit'):
                kwargs["queryset"] = SubjectVisit.objects.filter(id=request.GET.get('subject_visit'))
        return super(BaseSubjectModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    actions = [
        export_as_csv_action(
            description="Export to CSV file",
            fields=[],
            delimiter=',',
            exclude=['subject_visit', 'user_created', 'user_modified', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'subject_visit__appointment__registered_subject__subject_identifier',
                 'gender': 'subject_visit__appointment__registered_subject__gender',
                 'dob': 'subject_visit__appointment__registered_subject__dob',
                 'screened': 'subject_visit__appointment__registered_subject__screening_datetime',
                 'registered': 'subject_visit__appointment__registered_subject__registration_datetime',
                 'visit_code': 'subject_visit__appointment__visit_definition__code',
                 'visit_reason': 'subject_visit__reason',
                 'visit_study_status': 'subject_visit__study_status'}),
        )]
