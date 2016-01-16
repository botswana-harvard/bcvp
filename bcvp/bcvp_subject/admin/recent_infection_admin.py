from django.contrib import admin

from ..models import RecentInfection

from .base_subject_model_admin import BaseSubjectModelAdmin


class RecentInfectionAdmin(BaseSubjectModelAdmin):
    list_display = (
        'subject_identifier',
        'first_name',
        'initials',
        'born',
        'specimen_identifier',
        'cell',
        'cell_alt')
    search_fields = (
        'subject_identifier', 'identity', 'initials',
        'specimen_identifier', 'contact_cell_number', 'alt_contact_cell_number')
admin.site.register(RecentInfection, RecentInfectionAdmin)
