from django.contrib import admin

from ..forms import SubjectDeathReportForm
from ..models import SubjectDeathReport

from .base_subject_model_admin import BaseSubjectModelAdmin


class SubjectDeathReportAdmin(BaseSubjectModelAdmin):

    form = SubjectDeathReportForm
    fields = (
        "subject_visit",
        "report_datetime",
        "death_date",
        "cause",
        "cause_other",
        "perform_autopsy",
        "death_cause",
        "cause_category",
        "cause_category_other",
        "diagnosis_code",
        "diagnosis_code_other",
        "illness_duration",
        "medical_responsibility",
        "participant_hospitalized",
        "reason_hospitalized",
        "reason_hospitalized_other",
        "days_hospitalized",
        "comment")
    radio_fields = {
        "cause": admin.VERTICAL,
        "perform_autopsy": admin.VERTICAL,
        "participant_hospitalized": admin.VERTICAL,
        "cause_category": admin.VERTICAL,
        "diagnosis_code": admin.VERTICAL,
        "medical_responsibility": admin.VERTICAL,
        "reason_hospitalized": admin.VERTICAL}

admin.site.register(SubjectDeathReport, SubjectDeathReportAdmin)
