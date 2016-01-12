from edc_lab.lab_packing.forms import BasePackingListForm, BasePackingListItemForm

from ..models import SubjectRequisition, PackingList, PackingListItem, Aliquot


class PackingListForm (BasePackingListForm):

    def clean(self):
        self.requisition = [SubjectRequisition, Aliquot]
        return super(PackingListForm, self).clean()

    class Meta:
        model = PackingList


class PackingListItemForm (BasePackingListItemForm):

    def clean(self):
        self.requisition = [SubjectRequisition, Aliquot]
        return super(BasePackingListItemForm, self).clean()

    class Meta:
        model = PackingListItem
