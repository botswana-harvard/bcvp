from edc_lab.lab_requisition.classes import site_requisitions

from .models import SubjectRequisition

from bcvp.bcvp.constants import SUBJECT

site_requisitions.register(SUBJECT, SubjectRequisition)
