# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.contrib import admin

from .models import Workshop, Instructor, Rate, Order, OrderItem


class InstructorInline(admin.TabularInline):
    model = Instructor.workshops.through
    extra = 1


class RateInline(admin.TabularInline):
    model = Rate
    extra = 1


class WorkshopAdmin(admin.ModelAdmin):
    inlines = [InstructorInline, RateInline]
    prepopulated_fields = {'slug': ('title', 'start_date')}
    list_display = ('title', 'start_date', 'end_date', 'url', 'live',
                    'capacity', 'total_tickets_sold', 'sales_open',
                    'seats_available')

    # Show 'draft' in the admin is a bit confusing with the default django
    # widgets, so inverting makes sense here
    def live(self, obj):
        return not obj.draft
    live.boolean = True
    live.short_description = 'Visible'

    def seats_available(self, obj):
        return not obj.is_at_capacity
    seats_available.boolean = True
    seats_available.short_description = 'Seats available'


class RateAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'workshop')


class OrderItemInline(admin.TabularInline):
    can_delete = False
    model = OrderItem
    extra = 0
    readonly_fields = ('rate', 'name')
    fields = ('rate', 'name')

    def has_add_permission(self, request):
        return False


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


class OrderWorkshopFilter(admin.SimpleListFilter):
    title = 'workshop'
    parameter_name = 'workshop'

    def lookups(self, request, model_admin):
        return Workshop.objects.values_list('pk', 'title') \
                .order_by('start_date')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(orderitem__rate__workshop=self.value())


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ('contact_name', 'contact_email', 'order_total',
                       'billed_total', 'billed_datetime', 'transaction_id')
    list_display = ('contact_name', 'contact_email', 'order_total',
                    'order_datetime', 'billed_total', 'billed_datetime',
                    'transaction_id')
    list_display_links = ('contact_name', 'contact_email')
    list_filter = (OrderPaidListFilter, OrderWorkshopFilter, 'order_datetime',
                   'contact_email')


class OrderItemWorkshopFilter(admin.SimpleListFilter):
    title = 'workshop'
    parameter_name = 'workshop'

    def lookups(self, request, model_admin):
        return Workshop.objects.values_list('pk', 'title') \
                .order_by('start_date')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(rate__workshop=self.value())


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


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'workshop', 'rate',
                    'order_transaction_id')
    list_filter = (OrderItemWorkshopFilter, OrderItemPaidListFilter)
    readonly_fields = ('order', 'rate', 'name', 'email')

    def order_transaction_id(self, obj):
        return obj.order.transaction_id
    order_transaction_id.admin_order_field = 'order__transaction_id'

    def workshop(self, obj):
        return obj.rate.workshop.title
    workshop.admin_order_field = 'rate__workshop__title'


admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Instructor)
admin.site.register(Rate, RateAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
