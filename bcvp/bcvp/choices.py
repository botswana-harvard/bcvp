from edc_constants.constants import (
    OTHER, UNSCHEDULED, SCHEDULED, MISSED_VISIT, LOST_VISIT,
    COMPLETED_PROTOCOL_VISIT, FAILED_ELIGIBILITY, PARTICIPANT, ON_STUDY, OFF_STUDY, NOT_APPLICABLE)


ADHERENCE4DAY_CHOICE = (
    ('Zero', _('Zero days')),
    ('One day', _('One day')),
    ('Two days', _('Two days')),
    ('Three days', _('Three days')),
    ('Four days', _('Four days')),
    ('not_answering', _('Don\'t want to answer')),
)

ADHERENCE4WK_CHOICE = (
    ('Very poor', _('Very poor')),
    ('Poor', _('Poor')),
    ('Fair', _('Fair')),
    ('Good', _('Good')),
    ('Very good', _('Very good')),
    ('not_answering', _('Don\'t want to answer')),
)

ALCOHOL_SEX = (
    ('Neither of us', _('Neither of us')),
    ('My partner', _('My partner')),
    ('Myself', _('Myself')),
    ('Both of us', _('Both of us')),
    ('not_answering', _('Don\'t want to answer')),
)

CATTLEPOSTLANDS_CHOICE = (
    (NOT_APPLICABLE, _('Not Applicable')),
    ('Farm/lands', _('Farm/lands')),
    ('Cattle post', _('Cattle post')),
    ('Other community', _('Other community, specify:')),
    ('not_answering', _('Don\'t want to answer')),
)

INTERCOURSE_TYPE = (
    ('Vaginal', _('Vaginal sex')),
    ('Anal', _('Anal sex')),
    ('Both', _('Both vaginal and anal sex')),
)

LENGTHRESIDENCE_CHOICE = (
    ('Less than 6 months', _('Less than 6 months')),
    ('6 months to 12 months', _('6 months to 12 months')),
    ('1 to 5 years', _('1 to 5 years')),
    ('More than 5 years', _('More than 5 years')),
    ('not_answering', _('Don\'t want to answer')),
)

MAIN_PARTNER_RESIDENCY = (
    ('In this community', _('In this community')),
    ('On farm/cattle post', _('On farm/cattle post')),
    ('Outside this community', _('Outside this community')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)

NIGHTSAWAY_CHOICE = (
    ('zero', _('Zero nights')),
    ('1-6 nights', _('1-6 nights')),
    ('1-2 weeks', _('1-2 weeks')),
    ('3 weeks to less than 1 month', _('3 weeks to less than 1 month')),
    ('1-3 months', _('1-3 months')),
    ('4-6 months', _('4-6 months')),
    ('more than 6 months', _('more than 6 months')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

NO_MEDICAL_CARE = (
    ('Did not feel sick', _('Did not feel sick')),
    ('Did not know I should get HIV care', _('Did not know I should get HIV care')),
    ('Did not have time due to work responsibilities', _('Did not have time due to work responsibilities')),
    ('Did not have time due to family/childcare responsibilities', _('Did not have time due to family/childcare responsibilities')),
    ('Transportation costs', _('Transportation costs')),
    ('Was afraid of someone (friends/family) seeing me at the HIV clinic', _('Was afraid of someone (friends/family) seeing me at the HIV clinic')),
    ('Traditional healer advised against going', _('Traditional healer advised against going')),
    ('Religious beliefs', _('Religious beliefs')),
    ('Cultural beliefs', _('Cultural beliefs')),
    ('OTHER', _('Other, specify:')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

RELATIONSHIP_TYPE = (
    ('Longterm partner', _('Longterm partner (>2 years) or spouse')),
    ('Boyfriend/Girlfriend', _('Boyfriend/Girlfriend')),
    ('Casual', _('Casual (known) partner')),
    ('One time partner', _('One time partner (previously unknown)')),
    ('Commercial sex worker', _('Commercial sex worker')),
    ('Other, specify', _('Other, specify')),
)

SEX_REGULARITY = (
    ('All of the time', _('All of the time')),
    ('Sometimes', _('Sometimes')),
    ('Never', _('Never')),
)

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

WHYNOARV_CHOICE = (
    ('Did not feel sick', _('Did not feel sick')),
    ('Was afraid treatment would make me feel bad/sick', _('Was afraid treatment  would make me feel bad/sick')),
    ('Difficulty finding someone to go with me for counseling (mopati)', _('Difficulty finding someone to go with me for counseling (mopati)')),
    ('Hard due to work responsibilities', _('Hard due to work responsibilities')),
    ('Hard due to family/childcare responsibilities', _('Hard due to family/childcare responsibilities')),
    ('Transportation costs', _('Transportation costs')),
    ('Was afraid of someone (friends/family) seeing me at the HIV clinic', _('Was afraid of someone (friends/family) seeing me at the HIV clinic')),
    ('Sexual partner advised against taking', _('Sexual partner advised against taking')),
    ('Family or friends advised against taking', _('Family or friends advised against taking')),
    ('Traditional healer advised against taking', _('Traditional healer advised against taking')),
    ('Religious beliefs', _('Religious beliefs')),
    ('Cultural beliefs', _('Cultural beliefs')),
    ('High CD4', _('High CD4')),
    ('Other', _('Other, specify:')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

WHYARVSTOP_CHOICE = (
    ('Did not feel they were helping', _('Did not feel they were helping')),
    ('ARVs made me feel bad or sick', _('ARVs made me feel bad or sick')),
    ('Difficulty finding someone to go with me for counseling (mopati)', _('Difficulty finding someone to go with me for counseling (mopati)')),
    ('Hard due to work responsibilities', _('Hard due to work responsibilities')),
    ('Hard due to family/childcare responsibilities', _('Hard due to family/childcare responsibilities')),
    ('Doctor or nurse at clinic told me to stop', _('Doctor or nurse at clinic told me to stop')),
    ('Transportation costs', _('Transportation costs')),
    ('Was afraid of someone (friends/family) seeing me at the HIV clinic', _('Was afraid of someone (friends/family) seeing me at the HIV clinic')),
    ('Sexual partner advised against taking', _('Sexual partner advised against taking')),
    ('Family or friends advised against taking', _('Family or friends advised against taking')),
    ('Traditional healer advised against taking', _('Traditional healer advised against taking')),
    ('Religious beliefs', _('Religious beliefs')),
    ('Cultural beliefs', _('Cultural beliefs')),
    ('Other', _('Other, specify:')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)
