from edc_constants.constants import (
    OTHER, UNSCHEDULED, SCHEDULED, MISSED_VISIT, LOST_VISIT,
    COMPLETED_PROTOCOL_VISIT, FAILED_ELIGIBILITY, PARTICIPANT, ON_STUDY, OFF_STUDY, NOT_APPLICABLE)


ADHERENCE4DAY_CHOICE = (
    ('Zero', 'Zero days'),
    ('One day', 'One day'),
    ('Two days', 'Two days'),
    ('Three days', 'Three days'),
    ('Four days', 'Four days'),
    ('not_answering', 'Don\'t want to answer'),
)

ADHERENCE4WK_CHOICE = (
    ('Very poor', 'Very poor'),
    ('Poor', 'Poor'),
    ('Fair', 'Fair'),
    ('Good', 'Good'),
    ('Very good', 'Very good'),
    ('not_answering', 'Don\'t want to answer'),
)

ALCOHOL_SEX = (
    ('Neither of us', 'Neither of us'),
    ('My partner', 'My partner'),
    ('Myself', 'Myself'),
    ('Both of us', 'Both of us'),
    ('not_answering', 'Don\'t want to answer'),
)

CATTLEPOSTLANDS_CHOICE = (
    (NOT_APPLICABLE, 'Not Applicable'),
    ('Farm/lands', 'Farm/lands'),
    ('Cattle post', 'Cattle post'),
    ('Other community', 'Other community, specify:'),
    ('not_answering', 'Don\'t want to answer'),
)

DAY_MON_YEAR = (
    ('days', 'Days'),
    ('months', 'Months'),
    ('years', 'Years'),
)

INTERCOURSE_TYPE = (
    ('Vaginal', 'Vaginal sex'),
    ('Anal', 'Anal sex'),
    ('Both', 'Both vaginal and anal sex'),
)

LENGTHRESIDENCE_CHOICE = (
    ('Less than 6 months', 'Less than 6 months'),
    ('6 months to 12 months', '6 months to 12 months'),
    ('1 to 5 years', '1 to 5 years'),
    ('More than 5 years', 'More than 5 years'),
    ('not_answering', 'Don\'t want to answer'),
)

MAIN_PARTNER_RESIDENCY = (
    ('In this community', 'In this community'),
    ('On farm/cattle post', 'On farm/cattle post'),
    ('Outside this community', 'Outside this community'),
    ('Don\'t want to answer', 'Don\'t want to answer'),
)

NIGHTSAWAY_CHOICE = (
    ('zero', 'Zero nights'),
    ('1-6 nights', '1-6 nights'),
    ('1-2 weeks', '1-2 weeks'),
    ('3 weeks to less than 1 month', '3 weeks to less than 1 month'),
    ('1-3 months', '1-3 months'),
    ('4-6 months', '4-6 months'),
    ('more than 6 months', 'more than 6 months'),
    ('not_sure', 'I am not sure'),
    ('not_answering', 'Don\'t want to answer'),
)

NO_MEDICAL_CARE = (
    ('Did not feel sick', 'Did not feel sick'),
    ('Did not know I should get HIV care', 'Did not know I should get HIV care'),
    ('Did not have time due to work responsibilities', 'Did not have time due to work responsibilities'),
    ('Did not have time due to family/childcare responsibilities',
     'Did not have time due to family/childcare responsibilities'),
    ('Transportation costs', 'Transportation costs'),
    ('Was afraid of someone (friends/family) seeing me at the HIV clinic',
     'Was afraid of someone (friends/family) seeing me at the HIV clinic'),
    ('Traditional healer advised against going', 'Traditional healer advised against going'),
    ('Religious beliefs', 'Religious beliefs'),
    ('Cultural beliefs', 'Cultural beliefs'),
    ('OTHER', 'Other, specify:'),
    ('not_sure', 'I am not sure'),
    ('not_answering', 'Don\'t want to answer'),
)

RELATIONSHIP_TYPE = (
    ('Longterm partner', 'Longterm partner (>2 years) or spouse'),
    ('Boyfriend/Girlfriend', 'Boyfriend/Girlfriend'),
    ('Casual', 'Casual (known) partner'),
    ('One time partner', 'One time partner (previously unknown)'),
    ('Commercial sex worker', 'Commercial sex worker'),
    ('Other, specify', 'Other, specify'),
)

SEX_REGULARITY = (
    ('All of the time', 'All of the time'),
    ('Sometimes', 'Sometimes'),
    ('Never', 'Never'),
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
    (OFF_STUDY, 'off study'),
)

WHYNOARV_CHOICE = (
    ('Did not feel sick', 'Did not feel sick'),
    ('Was afraid treatment would make me feel bad/sick', 'Was afraid treatment  would make me feel bad/sick'),
    ('Difficulty finding someone to go with me for counseling (mopati)',
     'Difficulty finding someone to go with me for counseling (mopati)'),
    ('Hard due to work responsibilities', 'Hard due to work responsibilities'),
    ('Hard due to family/childcare responsibilities', 'Hard due to family/childcare responsibilities'),
    ('Transportation costs', 'Transportation costs'),
    ('Was afraid of someone (friends/family) seeing me at the HIV clinic',
     'Was afraid of someone (friends/family) seeing me at the HIV clinic'),
    ('Sexual partner advised against taking', 'Sexual partner advised against taking'),
    ('Family or friends advised against taking', 'Family or friends advised against taking'),
    ('Traditional healer advised against taking', 'Traditional healer advised against taking'),
    ('Religious beliefs', 'Religious beliefs'),
    ('Cultural beliefs', 'Cultural beliefs'),
    ('High CD4', 'High CD4'),
    ('Other', 'Other, specify:'),
    ('not_sure', 'I am not sure'),
    ('not_answering', 'Don\'t want to answer'),
)

WHYARVSTOP_CHOICE = (
    ('Did not feel they were helping', 'Did not feel they were helping'),
    ('ARVs made me feel bad or sick', 'ARVs made me feel bad or sick'),
    ('Difficulty finding someone to go with me for counseling (mopati)',
     'Difficulty finding someone to go with me for counseling (mopati)'),
    ('Hard due to work responsibilities', 'Hard due to work responsibilities'),
    ('Hard due to family/childcare responsibilities', 'Hard due to family/childcare responsibilities'),
    ('Doctor or nurse at clinic told me to stop', 'Doctor or nurse at clinic told me to stop'),
    ('Transportation costs', 'Transportation costs'),
    ('Was afraid of someone (friends/family) seeing me at the HIV clinic',
     'Was afraid of someone (friends/family) seeing me at the HIV clinic'),
    ('Sexual partner advised against taking', 'Sexual partner advised against taking'),
    ('Family or friends advised against taking', 'Family or friends advised against taking'),
    ('Traditional healer advised against taking', 'Traditional healer advised against taking'),
    ('Religious beliefs', 'Religious beliefs'),
    ('Cultural beliefs', 'Cultural beliefs'),
    ('Other', 'Other, specify:'),
    ('not_sure', 'I am not sure'),
    ('not_answering', 'Don\'t want to answer'),
)
