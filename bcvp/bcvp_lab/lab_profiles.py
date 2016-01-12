from edc_lab.lab_profile.classes import site_lab_profiles

from edc_lab.lab_profile.classes import LabProfile

from .models import (Aliquot, AliquotType, Receive, SubjectRequisition,
                     AliquotProfile, AliquotProfileItem, Panel)


class BaseMicrobiomeProfile(LabProfile):
    aliquot_model = Aliquot
    aliquot_type_model = AliquotType
    profile_model = AliquotProfile
    profile_item_model = AliquotProfileItem
    receive_model = Receive
    panel_model = Panel


class SubjectProfile(BaseMicrobiomeProfile):
    requisition_model = SubjectRequisition
    name = SubjectRequisition._meta.object_name
site_lab_profiles.register(SubjectProfile)
