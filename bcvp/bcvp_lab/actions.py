from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils import timezone

from .models import Order, OrderItem


def create_order(modeladmin, request, queryset):
    order_datetime = timezone.now()
    order = Order.objects.create(order_datetime=order_datetime)
    for aliquot in queryset:
        OrderItem.objects.create(order=order, aliquot=aliquot, order_datetime=order_datetime)
    change_url = reverse("admin:mb_lab_order_change", args=(order.pk, ))
    return HttpResponseRedirect(change_url)
create_order.short_description = "Create order from selected aliquots"
