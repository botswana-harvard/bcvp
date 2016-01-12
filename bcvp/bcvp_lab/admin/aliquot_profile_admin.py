from django.contrib import admin

from edc_base.modeladmin.admin import BaseTabularInline
from edc_lab.lab_profile.admin import BaseProfileAdmin, BaseProfileItemAdmin

from ..models import AliquotProfileItem, AliquotProfile


class AliquotProfileItemAdmin(BaseProfileItemAdmin):
    pass
admin.site.register(AliquotProfileItem, AliquotProfileItemAdmin)


class AliquotProfileItemInlineAdmin(BaseTabularInline):
    model = AliquotProfileItem


class AliquotProfileAdmin(BaseProfileAdmin):
    inlines = [AliquotProfileItemInlineAdmin]
admin.site.register(AliquotProfile, AliquotProfileAdmin)
