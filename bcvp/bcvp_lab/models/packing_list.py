from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_lab.lab_packing.models import PackingListMixin
from edc_sync.models import SyncModelMixin

from ..managers import PackingListManager


class PackingList(PackingListMixin, SyncModelMixin, BaseUuidModel):

    objects = PackingListManager()

    history = AuditTrail()

    @property
    def item_models(self):
        item_m = []
        item_m.append(models.get_model('bcvp_lab', 'SubjectRequisition'))
        item_m.append(models.get_model('bcvp_lab', 'Aliquot'))
        return item_m

    @property
    def packing_list_item_model(self):
        return models.get_model('bcvp_lab', 'PackingListItem')

    class Meta:
        app_label = "bcvp_lab"
        verbose_name = 'Packing List'
