# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.contrib import admin

from .models import Workshop


class WorkshopFilterBase(admin.SimpleListFilter):
    title = 'workshop'
    parameter_name = 'workshop'
    _filter = None

    def lookups(self, request, model_admin):
        return Workshop.objects.values_list('pk', 'title') \
                .order_by('start_date')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{self._filter: self.value()})


class OrderWorkshopListFilter(WorkshopFilterBase):
    _filter = 'orderitem__rate__workshop'


class OrderItemWorkshopListFilter(WorkshopFilterBase):
    _filter = 'rate__workshop'


class PaidFilterBase(admin.SimpleListFilter):
    title = 'payment status'
    parameter_name = 'paid'
    _filter = None

    def lookups(self, request, model_admin):
        return (
            ('true', 'Paid'),
            ('false', 'Not Paid'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        kwargs = {self._filter: ''}
        if value == 'true':
            return queryset.exclude(**kwargs)
        if value == 'false':
            return queryset.filter(**kwargs)


class OrderPaidListFilter(PaidFilterBase):
    _filter = 'billed_total'


class OrderItemPaidListFilter(PaidFilterBase):
    _filter = 'order__billed_total'
