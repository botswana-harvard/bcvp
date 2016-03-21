from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from ..models import RecentInfection

from .base_subject_model_admin import BaseSubjectModelAdmin


class RecentInfectionAdmin(BaseSubjectModelAdmin):

    fields = (
        'subject_identifier',
        'specimen_identifier',
        'result',
        'classification')

    list_display = (
        'subject_identifier',
        'first_name',
        'initials',
        'identity',
        'born',
        'specimen_identifier',
        'subject_cell',
        'subject_cell_alt')

    radio_fields = {
        "classification": admin.VERTICAL,
    }

    search_fields = (
        'subject_identifier', 'identity', 'initials',
        'specimen_identifier', 'subject_cell', 'subject_cell_alt')

    actions = [
        export_as_csv_action(
            description="Export to CSV file",
            fields=[],
            delimiter=',',
            exclude=['user_created', 'user_modified', 'hostname_created', 'hostname_modified', 'identity',
                     'gps_target_lon', 'gps_target_lat', 'first_name', 'dob', 'initials', 'subject_cell', 
                     'subject_cell_alt'],
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

admin.site.register(RecentInfection, RecentInfectionAdmin)
