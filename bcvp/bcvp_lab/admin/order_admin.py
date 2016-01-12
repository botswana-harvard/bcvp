from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline

from ..models import Order, OrderItem


class OrderItemInlineAdmin(BaseTabularInline):
    model = OrderItem
    fields = ('aliquot', 'panel', 'order_datetime', 'order_identifier', 'subject_identifier')
    readonly_fields = ('aliquot', 'order_identifier', 'subject_identifier')


class OrderItemAdmin(BaseModelAdmin):

    fields = ('aliquot', 'panel', 'order_datetime', 'order_identifier', 'subject_identifier')
    list_display = ('order_identifier', 'aliquot', 'panel', 'order_datetime', 'subject_identifier')
    search_fields = ('id', 'order__id', 'order_identifier', 'aliquot__aliquot_identifier',
                     'subject_identifier')
    readonly_fields = ('aliquot', 'order_identifier', 'subject_identifier')

admin.site.register(OrderItem, OrderItemAdmin)


class OrderAdmin(BaseModelAdmin):

    list_display = ('id', 'order_datetime', 'items')
    list_filter = ("order_datetime", )
    search_fields = ('id', )
    inlines = [OrderItemInlineAdmin, ]

admin.site.register(Order, OrderAdmin)
