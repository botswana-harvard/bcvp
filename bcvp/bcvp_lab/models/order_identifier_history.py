from edc_base.model.models import BaseUuidModel
from edc_identifier.models import BaseIdentifierModel
from edc_sync.models import SyncModelMixin


class OrderIdentifierHistory(BaseIdentifierModel, SyncModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcvp_lab"
