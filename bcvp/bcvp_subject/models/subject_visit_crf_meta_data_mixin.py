from edc_meta_data.models import CrfMetaDataMixin
from edc_constants.constants import (
    FAILED_ELIGIBILITY, UNSCHEDULED, COMPLETED_PROTOCOL_VISIT, NEG, POS, OFF_STUDY)


class SubjectVisitCrfMetaDataMixin(CrfMetaDataMixin):

    def custom_post_update_crf_meta_data(self):
        """Custom methods that manipulate meta data on the post save.

        This method is called in the edc_meta_data signal."""
        if self.reason == FAILED_ELIGIBILITY:
            self.study_status = OFF_STUDY
        elif self.reason == UNSCHEDULED:
            self.change_to_unscheduled_visit(self.appointment)
        elif self.reason == COMPLETED_PROTOCOL_VISIT:
            self.study_status = OFF_STUDY
        else:
            self.required_for_subject_pos()
            self.required_for_subject_not_pos()
            self.required_labs_for_subject_neg()
            self.required_forms_for_subject_neg()
        return self

    def required_forms_for_subject_neg(self):
        """If attempt to change an offstudy to scheduled visit has been successful, ensure that
        necessary forms at 1000M are REQUIRED"""
        if self.enrollment_hiv_status == NEG or self.scheduled_rapid_test == NEG:
            if self.appointment.visit_definition.code == '1000M':
                model_names = [
                    'subjectlocator', 'subjectdemographics', 'subjectmedicalhistory',
                    'subjectobstericalhistory']
                for model_name in model_names:
                    self.crf_is_required(self.appointment, 'mb_subject', model_name)
                self.crf_is_not_required(self.appointment, 'mb_subject', 'subjectoffstudy')

    def required_for_subject_pos(self):
        if self.enrollment_hiv_status == POS or self.scheduled_rapid_test == POS:
            if self.appointment.visit_definition.code == '1000M':
                model_names = ['subjectclinicalhistory', 'subjectarvhistory', 'subjectarvpreg']
                for model_name in model_names:
                    self.crf_is_required(self.appointment, 'mb_subject', model_name)
            elif self.appointment.visit_definition.code == '2000M':
                model_names = ['subjectarvpreg', 'subjectlabdelclinic']
                for model_name in model_names:
                    self.crf_is_required(self.appointment, 'mb_subject', model_name)
                    for labs in ['Viral Load', 'Breast Milk (Storage)', 'Vaginal swab (Storage)',
                                 'Rectal swab (Storage)', 'Skin Swab (Storage)',
                                 'Vaginal Swab (multiplex PCR)', 'Hematology (ARV)',
                                 'CD4 (ARV)']:
                        self.requisition_is_required(self.appointment, 'bcvp_lab', 'subjectrequisition', labs)
            elif self.appointment.visit_definition.code in ['2010M', '2030M', '2060M', '2090M', '2120M']:
                model_names = ['subjectarvpost', 'subjectarvpostadh']
                for model_name in model_names:
                    self.crf_is_required(self.appointment, 'mb_subject', model_name)
                self.requisition_is_required(self.appointment, 'bcvp_lab', 'subjectrequisition', 'Viral Load')

    def required_for_subject_not_pos(self):
        if self.enrollment_hiv_status == NEG and self.scheduled_rapid_test != POS:
            if self.appointment.visit_definition.code in ['2010M', '2030M', '2060M', '2090M', '2120M']:
                self.crf_is_required(self.appointment, 'mb_subject', 'rapidtestresult')

    def required_labs_for_subject_neg(self):
        if self.enrollment_hiv_status == NEG and self.scheduled_rapid_test != POS:
            if self.appointment.visit_definition.code == '2000M':
                for labs in ['Breast Milk (Storage)', 'Vaginal swab (Storage)',
                             'Rectal swab (Storage)', 'Skin Swab (Storage)',
                             'Vaginal Swab (multiplex PCR)', 'Hematology (ARV)',
                             'CD4 (ARV)']:
                    self.requisition_is_required(self.appointment, 'bcvp_lab', 'subjectrequisition', labs)
            if self.appointment.visit_definition.code == '2010M':
                self.requisition_is_required(
                    self.appointment, 'bcvp_lab', 'subjectrequisition', 'Breast Milk (Storage)')

    class Meta:
        abstract = True
