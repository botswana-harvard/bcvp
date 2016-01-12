from django.contrib import admin

from ..models import SubjectOffStudy
from ..forms import SubjectOffStudyForm
from .base_subject_model_admin import BaseSubjectModelAdmin


class SubjectOffStudyAdmin(BaseSubjectModelAdmin):

    form = SubjectOffStudyForm

    fields = (
        'subject_visit',
        'report_datetime',
        'offstudy_date',
        'reason',
        'reason_other',
        'comment')

admin.site.register(SubjectOffStudy, SubjectOffStudyAdmin)
