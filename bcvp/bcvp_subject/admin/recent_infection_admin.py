from django.contrib import admin

from ..models import RecentInfection

from .base_subject_model_admin import BaseSubjectModelAdmin


class RecentInfectionAdmin(BaseSubjectModelAdmin):

    fields = (
        'subject_identifier',
        'first_name',
        'dob',
        'initials',
        'identity',
        'test_date',
        'specimen_identifier',
        'drawn_datetime',
        'result',
        'gps_lon',
        'gps_lat',
        'subject_cell',
        'subject_cell_alt')

    list_display = (
        'subject_identifier',
        'first_name',
        'initials',
        'born',
        'specimen_identifier',
        'subject_cell',
        'subject_cell_alt')

    search_fields = (
        'subject_identifier', 'identity', 'initials',
        'specimen_identifier', 'subject_cell', 'subject_cell_alt')

admin.site.register(RecentInfection, RecentInfectionAdmin)
