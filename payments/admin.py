# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.contrib import admin

from import_export.admin import ExportMixin

from .admin_filters import (OrderPaidListFilter, OrderWorkshopListFilter,
                            OrderItemPaidListFilter,
                            OrderItemWorkshopListFilter,
                            OrderRefundedListFilter,
                            OrderItemRefundedListFilter)
from .models import Workshop, Instructor, Rate, Order, OrderItem, PosterOption


class InstructorInline(admin.TabularInline):
    model = Instructor.workshops.through
    extra = 1


class RateInline(admin.TabularInline):
    model = Rate
    extra = 1
    fields = ('name', 'price', 'capacity', 'sales_open', 'private',
              'discount_code')


class OrderItemInline(admin.TabularInline):
    can_delete = False
    model = OrderItem
    extra = 0
    readonly_fields = ('rate', 'name', 'poster')
    fields = ('rate', 'name', 'poster')

    def has_add_permission(self, request):
        return False


class PosterOptionInline(admin.TabularInline):
    model = PosterOption
    extra = 1


class WorkshopAdmin(admin.ModelAdmin):
    inlines = [RateInline, PosterOptionInline, InstructorInline]
    prepopulated_fields = {'slug': ('title', 'start_date')}
    list_display = ('title', 'start_date', 'end_date', 'url', 'live',
                    'total_tickets_sold', 'seats_available')

    # inject jQuery and our WorkshopAdmin specific JavaScript file
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'js/workshop.js'
        )

    # Show 'draft' in the admin is a bit confusing with the default django
    # widgets, so inverting makes sense here
    def live(self, obj):
        return not obj.draft
    live.boolean = True
    live.short_description = 'Visible'

    def seats_available(self, obj):
        # Admins forms wouldn't implicitly interpret this as boolean
        return len(obj.rate_set.filter(private=False, sold_out=False)) != 0
    seats_available.boolean = True
    seats_available.short_description = 'Seats available'


class OrderAdmin(ExportMixin, admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ('contact_name', 'contact_email', 'order_total',
                       'transaction_id')
    list_display = ('contact_name', 'contact_email', 'order_total', 'paid',
                    'refunded', 'order_datetime', 'billed_datetime',
                    'transaction_id')
    list_display_links = ('contact_name', 'contact_email')
    list_filter = (OrderWorkshopListFilter, OrderPaidListFilter,
                   OrderRefundedListFilter, 'order_datetime', 'contact_email')

    def paid(self, obj):
        return obj.billed_total != ''
    paid.admin_order_field = 'billed_total'
    paid.boolean = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OrderItemAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'workshop', 'rate', 'poster', 'paid',
                    'refunded', 'order_transaction_id')
    list_filter = (OrderItemWorkshopListFilter, OrderItemPaidListFilter,
                   OrderItemRefundedListFilter)
    readonly_fields = ('order', 'rate', 'poster', 'name', 'email')

    def order_transaction_id(self, obj):
        return obj.order.transaction_id
    order_transaction_id.admin_order_field = 'order__transaction_id'

    def workshop(self, obj):
        return obj.rate.workshop.title
    workshop.admin_order_field = 'rate__workshop__title'

    def paid(self, obj):
        return obj.order.billed_total != ''
    paid.admin_order_field = 'order__billed_total'
    paid.boolean = True

    def refunded(self, obj):
        return obj.order.refunded
    refunded.admin_order_field = 'order__refunded'
    refunded.boolean = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class InstructorAdmin(admin.ModelAdmin):
    # This hides `Instructors` on the admin changelist page
    def get_model_perms(self, request):
        return {}


admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
