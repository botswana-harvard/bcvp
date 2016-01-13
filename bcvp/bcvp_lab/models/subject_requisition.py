from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models.base_uuid_model import BaseUuidModel
from lab_requisition.models import RequisitionModelMixin
from edc_meta_data.managers import RequisitionMetaDataManager
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models.crf_model_mixin import CrfModelMixin, CrfModelManager

from bcvp.bcvp_subject.models import SubjectVisit

from .aliquot import Aliquot
from .aliquot_type import AliquotType
from .packing_list import PackingList
from .panel import Panel


class SubjectRequisitionManager(CrfModelManager):

    def get_by_natural_key(self, requisition_identifier):
        return self.get(requisition_identifier=requisition_identifier)


class SubjectRequisition(CrfModelMixin, RequisitionModelMixin, SyncModelMixin, BaseUuidModel):

    visit_model = SubjectVisit

    visit_model_attr = 'subject_visit'

    aliquot_model = Aliquot

    subject_visit = models.ForeignKey(SubjectVisit)

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    aliquot_type = models.ForeignKey(AliquotType)

    panel = models.ForeignKey(Panel)

    objects = SubjectRequisitionManager()

    history = AuditTrail()

    entry_meta_data_manager = RequisitionMetaDataManager(SubjectVisit)

    def __unicode__(self):
        return '{0} {1}'.format(unicode(self.panel), self.requisition_identifier)

    def natural_key(self):
        return (self.requisition_identifier,)

    class Meta:
        app_label = "bcvp_lab"
        verbose_name = 'Subject Requisition'
        verbose_name_plural = 'Subject Requisition'
        unique_together = ('subject_visit', 'panel', 'is_drawn')
        ordering = ('-created', )
