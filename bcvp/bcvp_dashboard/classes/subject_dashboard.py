from edc_dashboard.subject import RegisteredSubjectDashboard

from bcvp.bcvp_lab.models import SubjectRequisition
from bcvp.bcvp_subject.models import SubjectVisit, SubjectConsent, SubjectLocator
from bcvp.bcvp_subject.models.subject_eligibility import SubjectEligibility


class SubjectDashboard(RegisteredSubjectDashboard):

    view = 'subject_dashboard'
    dashboard_url_name = 'subject_dashboard_url'
    dashboard_name = 'Subject Dashboard'
    urlpattern_view = 'bcvp_dashboard.views'
    template_name = 'subject_dashboard.html'
    urlpatterns = [
        RegisteredSubjectDashboard.urlpatterns[0][:-1] +
        '(?P<appointment_code>{appointment_code})/$'] + RegisteredSubjectDashboard.urlpatterns
    urlpattern_options = dict(
        RegisteredSubjectDashboard.urlpattern_options,
        dashboard_model=RegisteredSubjectDashboard.urlpattern_options['dashboard_model'] + '|subject_eligibility',
        dashboard_type='subject',
        appointment_code='1000', )

    def __init__(self, **kwargs):
        super(SubjectDashboard, self).__init__(**kwargs)
        self.subject_dashboard_url = 'subject_dashboard_url'
        self.visit_model = SubjectVisit
        self.dashboard_type_list = ['subject']
        self.membership_form_category = ['subject']
        self.dashboard_models['subject_eligibility'] = SubjectEligibility
        self.dashboard_models['subject_consent'] = SubjectConsent
        self.dashboard_models['visit'] = SubjectVisit
        self.requisition_model = SubjectRequisition
        self._locator_model = SubjectLocator

    def get_context_data(self, **kwargs):
        super(SubjectDashboard, self).get_context_data(**kwargs)
        self.context.update(
            home='bcvp',
            search_name='subject',
            title='Subject Dashboard',
            subject_dashboard_url=self.subject_dashboard_url,
            subject_consent=self.consent,
            local_results=self.render_labs(),
        )
        return self.context

    @property
    def consent(self):
        self._consent = None
        try:
            self._consent = SubjectConsent.objects.get(subject_identifier=self.subject_identifier)
        except SubjectConsent.DoesNotExist:
            self._consent = None
        return self._consent

    def get_locator_scheduled_visit_code(self):
        """ Returns visit where the locator is scheduled, TODO: maybe search visit definition for this?."""
        return '1000'

    @property
    def subject_locator(self):
        return self.locator_model.objects.get(
            subject_visit__appointment__registered_subject__subject_identifier=self.subject_identifier)

    @property
    def subject_identifier(self):
        return self.registered_subject.subject_identifier

    @property
    def locator_model(self):
        return SubjectLocator
