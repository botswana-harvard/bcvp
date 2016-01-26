from django.contrib import admin

from ..forms import RecentPartnerForm
from ..models import RecentPartner


from .base_subject_model_admin import BaseSubjectModelAdmin


class RecentPartnerAdmin(BaseSubjectModelAdmin):

    form = RecentPartnerForm

    fields = (
        "subject_visit",
        "rel_type",
        "rel_type_other",
        "partner_residency",
        "partner_age",
        "partner_gender",
        "last_sex_contact",
        "last_sex_period",
        "first_sex_contact",
        "first_sex_period",
        "regular_sex",
        "having_sex",
        "having_sex_reg",
        "alcohol_before_sex",
        "partner_status",
        "partner_arv",
        "status_disclosure",
        "multiple_partners",
        "intercourse_type")

    radio_fields = {
        "rel_type": admin.VERTICAL,
        "partner_residency": admin.VERTICAL,
        "partner_gender": admin.VERTICAL,
        "having_sex": admin.VERTICAL,
        "having_sex_reg": admin.VERTICAL,
        "alcohol_before_sex": admin.VERTICAL,
        "partner_status": admin.VERTICAL,
        "partner_arv": admin.VERTICAL,
        "status_disclosure": admin.VERTICAL,
        "multiple_partners": admin.VERTICAL,
        "intercourse_type": admin.VERTICAL,
        "last_sex_period": admin.VERTICAL,
        "first_sex_period": admin.VERTICAL,
    }

admin.site.register(RecentPartner, RecentPartnerAdmin)
