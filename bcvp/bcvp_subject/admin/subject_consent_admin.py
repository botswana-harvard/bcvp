from django.contrib import admin
from collections import OrderedDict

from edc_base.modeladmin.admin import BaseModelAdmin
from edc_registration.models import RegisteredSubject
from edc_consent.actions import flag_as_verified_against_paper, unflag_as_verified_against_paper
from edc_export.actions import export_as_csv_action

from ..forms import SubjectConsentForm
from ..models import SubjectConsent


class SubjectConsentAdmin(BaseModelAdmin):

    form = SubjectConsentForm

    fields = ('registered_subject',
              'first_name',
              'last_name',
              'initials',
              'language',
              'study_site',
              'is_literate',
              'witness_name',
              'consent_datetime',
              'dob',
              'is_dob_estimated',
              'citizen',
              'identity',
              'identity_type',
              'confirm_identity',
              'comment',
              'consent_reviewed',
              'study_questions',
              'assessment_score',
              'consent_signature',
              'consent_copy')
    actions = [flag_as_verified_against_paper, unflag_as_verified_against_paper]

    radio_fields = {
        'assessment_score': admin.VERTICAL,
        'citizen': admin.VERTICAL,
        'consent_copy': admin.VERTICAL,
        'consent_reviewed': admin.VERTICAL,
        'consent_signature': admin.VERTICAL,
        'identity_type': admin.VERTICAL,
        'is_dob_estimated': admin.VERTICAL,
        'is_literate': admin.VERTICAL,
        'language': admin.VERTICAL,
        'study_questions': admin.VERTICAL}

    list_display = ('subject_identifier',
                    'registered_subject',
                    'is_verified',
                    'is_verified_datetime',
                    'first_name',
                    'initials',
                    'gender',
                    'dob',
                    'consent_datetime',
                    'created',
                    'modified',
                    'user_created',
                    'user_modified')
    list_filter = ('language',
                   'is_verified',
                   'is_literate',
                   'identity_type')

    actions = [
        export_as_csv_action(
            description="CSV Export of Subject Consent",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified', 'last_name', 'identity', 'confirm_identity', 'first_name'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'registered_subject__subject_identifier',
                 'gender': 'registered_subject__gender',
                 'dob': 'registered_subject__dob',
                 'registered': 'registered_subject__registration_datetime'}),
        )]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(
                    id__exact=request.GET.get('registered_subject', 0))
            else:
                self.readonly_fields = list(self.readonly_fields)
                try:
                    self.readonly_fields.index('registered_subject')
                except ValueError:
                    self.readonly_fields.append('registered_subject')
        return super(SubjectConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectConsent, SubjectConsentAdmin)
