# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
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

    def lookups(self, request, model_admin):
        workshops = Workshop.objects.values_list('pk', 'title', 'start_date') \
                                    .order_by('start_date')
        return [(w[0], '%s (%s)' % (w[1], w[2])) for w in workshops]


class OrderWorkshopListFilter(WorkshopFilterBase):
    def queryset(self, request, queryset):
        if self.value():
            qs = queryset.filter(orderitem__rate__workshop=self.value())
            return qs.distinct()


class OrderItemWorkshopListFilter(WorkshopFilterBase):
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(rate__workshop=self.value())


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


class RefundedFilterBase(admin.SimpleListFilter):
    title = 'refund status'
    parameter_name = 'refunded'
    _filter = None

    def lookups(self, request, model_admin):
        return (
            ('true', 'Refunded'),
            ('false', 'Not Refunded'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        kwargs = {self._filter: False}
        if value == 'true':
            return queryset.exclude(**kwargs)
        if value == 'false':
            return queryset.filter(**kwargs)


class OrderPaidListFilter(PaidFilterBase):
    _filter = 'billed_total'


class OrderItemPaidListFilter(PaidFilterBase):
    _filter = 'order__billed_total'


class OrderRefundedListFilter(RefundedFilterBase):
    _filter = 'refunded'


class OrderItemRefundedListFilter(RefundedFilterBase):
    _filter = 'order__refunded'
