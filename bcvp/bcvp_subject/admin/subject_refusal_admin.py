from collections import OrderedDict

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc_export.actions import export_as_csv_action

from ..forms import SubjectRefusalForm
from ..models import SubjectRefusal, SubjectEligibility


class SubjectRefusalAdmin(BaseModelAdmin):

    form = SubjectRefusalForm

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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject_eligibility":
            if request.GET.get('subject_eligibility'):
                kwargs["queryset"] = SubjectEligibility.objects.filter(id=request.GET.get('subject_eligibility'))
        return super(SubjectRefusalAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(SubjectRefusal, SubjectRefusalAdmin)
