from collections import OrderedDict

from edc_visit_schedule.classes import (
    VisitScheduleConfiguration, site_visit_schedules, MembershipFormTuple, ScheduleTuple)

from ..models import SubjectVisit, SubjectConsent

from .entries import subject_crf_entries, subject_requisition_entries


class SubjectVisitSchedule(VisitScheduleConfiguration):

    name = 'subject survey schedule'
    app_label = 'bcvp_subject'

    membership_forms = OrderedDict({'subject': MembershipFormTuple(
        'subject', SubjectConsent, True), })

    schedules = OrderedDict({
        'Subject Survey': ScheduleTuple('Subject Survey', 'subject', None, None), })

    visit_definitions = OrderedDict()

    visit_definitions['1000'] = {
        'title': 'Subject Survey',
        'time_point': 0,
        'base_interval': 0,
        'base_interval_unit': 'D',
        'window_lower_bound': 0,
        'window_lower_bound_unit': 'D',
        'window_upper_bound': 0,
        'window_upper_bound_unit': 'D',
        'grouping': 'subject',
        'visit_tracking_model': SubjectVisit,
        'schedule': 'Subject Survey',
        'instructions': '',
        'requisitions': subject_requisition_entries,
        'entries': subject_crf_entries}

site_visit_schedules.register(SubjectVisitSchedule)
