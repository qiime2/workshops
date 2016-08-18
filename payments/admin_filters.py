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
    filter = None

    def lookups(self, request, model_admin):
        return Workshop.objects.values_list('pk', 'title') \
                .order_by('start_date')

    def queryset(self, request, queryset):
        if self.value():
            # TODO: set this filter from `filter`
            return queryset.filter(orderitem__rate__workshop=self.value())


class OrderWorkshopFilter(WorkshopFilterBase):
    filter = 'orderitem__rate__workshop'


class OrderItemWorkshopFilter(admin.SimpleListFilter):
    title = 'workshop'
    parameter_name = 'workshop'

    def lookups(self, request, model_admin):
        return Workshop.objects.values_list('pk', 'title') \
                .order_by('start_date')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(rate__workshop=self.value())


class OrderPaidListFilter(admin.SimpleListFilter):
    title = 'payment status'
    parameter_name = 'paid'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Paid'),
            ('false', 'Not Paid'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.exclude(billed_total='')
        if self.value() == 'false':
            return queryset.filter(billed_total='')


class OrderItemPaidListFilter(admin.SimpleListFilter):
    title = 'payment status'
    parameter_name = 'paid'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Paid'),
            ('false', 'Not Paid'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.exclude(order__billed_total='')
        if self.value() == 'false':
            return queryset.filter(order__billed_total='')
