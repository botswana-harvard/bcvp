from django.contrib import admin

from edc_registration.models import RegisteredSubject
from edc_locator.admin import BaseLocatorModelAdmin

from ..forms import SubjectLocatorForm
from ..models import SubjectLocator


class SubjectLocatorAdmin(BaseLocatorModelAdmin):

    form = SubjectLocatorForm

    fields = (
        'registered_subject',
        'report_datetime',
        'date_signed',
        'mail_address',
        'home_visit_permission',
        'physical_address',
        'may_follow_up',
        'subject_cell',
        'subject_cell_alt',
        'subject_phone',
        'subject_phone_alt',
        'may_call_work',
        'subject_work_place',
        'subject_work_phone',
        'may_contact_someone',
        'contact_name',
        'contact_rel',
        'contact_physical_address',
        'contact_cell',
        'contact_phone',
        'successful_mode_of_contact')
    list_display = ('may_follow_up', 'may_call_work')

    list_filter = ('may_follow_up', 'may_call_work')

    search_fields = (
        'registered_subject__subject_identifier', 'subject_cell', 'subject_cell_alt',
        'subject_phone', 'subject_phone_alt', 'subject_work_place', 'subject_work_phone')

    radio_fields = {"home_visit_permission": admin.VERTICAL,
                    "may_follow_up": admin.VERTICAL,
                    "may_call_work": admin.VERTICAL,
                    "may_contact_someone": admin.VERTICAL,
                    'successful_mode_of_contact': admin.VERTICAL}

    actions = []  # do not allow export to CSV

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            kwargs["queryset"] = RegisteredSubject.objects.filter(id__exact=request.GET.get('registered_subject', 0))
        return super(SubjectLocatorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(SubjectLocator, SubjectLocatorAdmin)
