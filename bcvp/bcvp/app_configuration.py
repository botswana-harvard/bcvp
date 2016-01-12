from datetime import datetime, date

from edc_lab.lab_packing.models import DestinationTuple
from edc_lab.lab_profile.classes import ProfileItemTuple, ProfileTuple
from edc_configuration.base_app_configuration import BaseAppConfiguration
from edc_device import Device

from lis.labeling.classes import LabelPrinterTuple, ZplTemplateTuple, ClientTuple
from lis.specimen.lab_aliquot_list.classes import AliquotTypeTuple
from lis.specimen.lab_panel.classes import PanelTuple

from .constants import MIN_AGE_OF_CONSENT

study_start_datetime = datetime(2015, 12, 1, 0, 0, 0)
study_end_datetime = datetime(2016, 12, 1, 0, 0, 0)


class AppConfiguration(BaseAppConfiguration):

    global_configuration = {
        'dashboard':
            {'show_not_required': True,
             'allow_additional_requisitions': False,
             'show_drop_down_requisitions': True},
        'appointment':
            {'allowed_iso_weekdays': ('12345', False),
             'use_same_weekday': True,
             'default_appt_type': 'clinic',
             'appointments_per_day_max': 20,
             'appointments_days_forward': 15},
        'protocol': {
            'start_datetime': study_start_datetime,
            'end_datetime': study_end_datetime},
    }

    study_variables_setup = {
        'protocol_number': 'BHP078',
        'protocol_code': '078',
        'protocol_title': 'BHP078',
        'research_title': 'Botswana Canadian Vaccine Project',
        'study_start_datetime': study_start_datetime,
        'minimum_age_of_consent': MIN_AGE_OF_CONSENT,
        'maximum_age_of_consent': 18,
        'gender_of_consent': 'MF',
        'subject_identifier_seed': '10000',
        'subject_identifier_prefix': '000',
        'subject_identifier_modulus': '7',
        'subject_type': 'subject',
        'machine_type': 'SERVER',
        'hostname_prefix': '0000',
        'device_id': Device().device_id}

    holidays_setup = {
        'New Year': date(2016, 1, 1),
        'New Year Holiday': date(2016, 1, 2),
        'Good Friday': date(2016, 3, 25),
        'Easter Monday': date(2016, 3, 28),
        'Labour Day': date(2016, 5, 1),
        'Labour Day Holiday': date(2016, 5, 2),
        'Ascension Day': date(2016, 5, 5),
        'Sir Seretse Khama Day': date(2016, 7, 1),
        'President\'s Day': date(2016, 7, 18),
        'President\'s Day Holiday': date(2016, 7, 19),
        'Independence Day': date(2016, 9, 30),
        'Botswana Day Holiday': date(2016, 10, 1),
        'Christmas Day': date(2015, 12, 25),
        'Boxing Day': date(2015, 12, 26)}

    consent_type_setup = [
        {'app_label': 'bcvp_subject',
         'model_name': 'subjectconsent',
         'start_datetime': study_start_datetime,
         'end_datetime': study_end_datetime,
         'version': '1'}]

    study_site_setup = []

    lab_clinic_api_setup = {
        'panel': [PanelTuple('Research Blood Draw', 'TEST', 'WB')],
        'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                         AliquotTypeTuple('Plasma', 'PL', '32'),
                         AliquotTypeTuple('Serum', 'SERUM', '06'),
                         AliquotTypeTuple('Buffy Coat', 'BC', '16')]}

    lab_setup = {'bcvp': {
                 'destination': [DestinationTuple('BHHRL', 'Botswana-Harvard HIV Reference Laboratory',
                                                  'Gaborone', '3902671', 'bhhrl@bhp.org.bw')],
                 'panel': [PanelTuple('Research Blood Draw', 'TEST', 'WB')],
                 'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                                  AliquotTypeTuple('Plasma', 'PL', '32'),
                                  AliquotTypeTuple('Serum', 'SERUM', '06'),
                                  AliquotTypeTuple('Buffy Coat', 'BC', '16')],
                 'profile': [ProfileTuple('Research Blood Draw', 'WB')],
                 'profile_item': [ProfileItemTuple('Research Blood Draw', 'PL', 1.0, 3),
                                  ProfileItemTuple('Research Blood Draw', 'BC', 0.5, 1)]}}

    labeling_setup = {
        'label_printer': [LabelPrinterTuple('Zebra_Technologies_ZTC_GK420t',
                                            'localhost', '127.0.0.1', True)],
        'client': [
            ClientTuple(
                hostname='localhost',
                printer_name='Zebra_Technologies_ZTC_GK420t',
                cups_hostname='localhost',
                ip=None,
                aliases=None)],
        'zpl_template': [
            ZplTemplateTuple(
                'aliquot_label', (
                    ('^XA\n'
                     '~SD22'
                     '^FO310,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   '
                     '${aliquot_type} ${aliquot_count}${primary}^FS\n'
                     '^FO310,34^BY1,3.0^BCN,50,N,N,N\n'
                     '^BY^FD${aliquot_identifier}^FS\n'
                     '^FO310,92^A0N,20,20^FD${aliquot_identifier}^FS\n'
                     '^FO310,112^A0N,20,20^FD${subject_identifier} (${initials})^FS\n'
                     '^FO310,132^A0N,20,20^FDDOB: ${dob} ${gender}^FS\n'
                     '^FO310,152^A0N,25,20^FD${drawn_datetime}^FS\n'
                     '^XZ')
                ), True),
            ZplTemplateTuple(
                'requisition_label', (
                    ('^XA\n' +
                     ('^FO310,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   '
                      '${aliquot_type} ${aliquot_count}${primary}^FS\n') +
                     '^FO310,34^BY1,3.0^BCN,50,N,N,N\n'
                     '^BY^FD${requisition_identifier}^FS\n'
                     '^FO310,92^A0N,20,20^FD${requisition_identifier} ${panel}^FS\n'
                     '^FO310,112^A0N,20,20^FD${subject_identifier} (${initials})^FS\n'
                     '^FO310,132^A0N,20,20^FDDOB: ${dob} ${gender}^FS\n'
                     '^FO310,152^A0N,25,20^FD${drawn_datetime}^FS\n'
                     '^XZ')), True)]
    }
