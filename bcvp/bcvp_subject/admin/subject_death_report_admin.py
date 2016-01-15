from django.contrib import admin

from ..forms import SubjectDeathReportForm
from ..models import SubjectDeathReport

from .base_subject_model_admin import BaseSubjectModelAdmin


class SubjectDeathReportAdmin(BaseSubjectModelAdmin):

    form = SubjectDeathReportForm
    fields = (
        "report_datetime",
        "last_date_known_alive",
        "death_cause",
        "cause_other",
    )
    radio_fields = {
        "death_cause": admin.VERTICAL,
    }

admin.site.register(SubjectDeathReport, SubjectDeathReportAdmin)
