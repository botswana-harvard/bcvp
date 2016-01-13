from edc_visit_schedule.classes.visit_schedule_configuration import RequisitionPanelTuple, CrfTuple
from edc_constants.constants import NOT_REQUIRED, REQUIRED, ADDITIONAL, NOT_ADDITIONAL


subject_crf_entries = (
    CrfTuple(10L, u'bcvp_subject', u'subjectlocator', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(100L, u'bcvp_subject', u'residencymobility', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(110L, u'bcvp_subject', u'hivcareadherence', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(120L, u'bcvp_subject', u'sexualbehaviour', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(130L, u'bcvp_subject', u'recentpartner', REQUIRED, NOT_ADDITIONAL),
    CrfTuple(200L, u'bcvp_subject', u'subjectdeathreport', NOT_REQUIRED, ADDITIONAL),
    CrfTuple(210L, u'bcvp_subject', u'subjectoffstudy', NOT_REQUIRED, ADDITIONAL))

subject_requisition_entries = (
    RequisitionPanelTuple(
        10L, u'bcvp_lab', u'subjectrequisition',
        'Research Blood Draw', 'TEST', 'WB', NOT_REQUIRED, ADDITIONAL),
)
