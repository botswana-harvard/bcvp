from django.contrib import admin

from ..forms import SubjectDeathReportForm
from ..models import SubjectDeathReport, SubjectEligibility

from .base_subject_model_admin import BaseSubjectModelAdmin


class SubjectDeathReportAdmin(BaseSubjectModelAdmin):

    form = SubjectDeathReportForm
    fields = (
        "subject_eligibility",
        "report_datetime",
        "last_date_known_alive",
        "death_cause",
        "cause_other",
    )
    radio_fields = {
        "death_cause": admin.VERTICAL,
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject_eligibility":
            if request.GET.get('subject_eligibility'):
                kwargs["queryset"] = SubjectEligibility.objects.filter(id=request.GET.get('subject_eligibility'))
        return super(SubjectDeathReportAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(SubjectDeathReport, SubjectDeathReportAdmin)
