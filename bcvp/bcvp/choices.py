from edc_constants.constants import (
    OTHER, UNSCHEDULED, SCHEDULED, MISSED_VISIT, LOST_VISIT,
    COMPLETED_PROTOCOL_VISIT, FAILED_ELIGIBILITY, PARTICIPANT, ON_STUDY, OFF_STUDY)

STUDY_SITES = (
    ('10', 'Mochudi'),
)

VISIT_INFO_SOURCE = [
    (PARTICIPANT, 'Clinic visit with participant'),
    ('other_contact', 'Other contact with participant (for example telephone call)'),
    ('other_doctor', 'Contact with external health care provider/medical doctor'),
    ('family', 'Contact with family or designated person who can provide information'),
    ('chart', 'Hospital chart or other medical record'),
    (OTHER, 'Other')]

VISIT_REASON = [
    (SCHEDULED, 'Scheduled visit/contact'),
    (MISSED_VISIT, 'Missed Scheduled visit'),
    (UNSCHEDULED, 'Unscheduled visit at which lab samples or data are being submitted'),
    (LOST_VISIT, 'Lost to follow-up (use only when taking subject off study)'),
    (FAILED_ELIGIBILITY, 'Subject failed enrollment eligibility'),
    (COMPLETED_PROTOCOL_VISIT, 'Subject has completed the study')]

OFF_STUDY_REASON = [
    ('moved', ' Subject will be moving out of study area or unable to stay in study area'),
    ('lost_no_contact', 'Lost to follow-up, unable to locate'),
    ('lost_contacted', 'Lost to follow-up, contacted but did not come to study clinic'),
    ('complete',
        ('Completion of protocol required period of time for observation '
         '(see Study Protocol for definition of Completion.) [skip to end of form]')),
    ('death',
        ('Participant death (complete the DEATH REPORT FORM AF005) '
         '(For EAE Reporting requirements see EAE Reporting Manual)')),
    (OTHER, 'Other'),
]

VISIT_STUDY_STATUS = (
    (ON_STUDY, 'on study'),
    (OFF_STUDY, 'off study')
)
