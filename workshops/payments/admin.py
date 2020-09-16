from django.contrib import admin
from django.urls import resolve
from django.utils.html import format_html_join, format_html

import markdownx

from .admin_filters import (OrderPaidListFilter, OrderWorkshopListFilter,
                            OrderItemPaidListFilter,
                            OrderItemWorkshopListFilter,
                            OrderRefundedListFilter,
                            OrderItemRefundedListFilter)
from .models import (
    Workshop, Instructor, Rate, Order, OrderItem, PosterOption, MeetingOption)


class InstructorInline(admin.TabularInline):
    model = Instructor.workshops.through
    extra = 1


class RateInline(admin.TabularInline):
    model = Rate
    extra = 1
    fields = ('name', 'price', 'capacity', 'max_order', 'sales_open', 'private',
              'parent', 'discount_code')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            resolved = resolve(request.path_info)
            workshop = self.parent_model.objects.get(pk=resolved.kwargs['object_id'])
            kwargs['queryset'] = Rate.objects.filter(workshop=workshop).select_related('workshop')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderItemInline(admin.TabularInline):
    can_delete = False
    model = OrderItem
    extra = 0
    readonly_fields = ('rate', 'name', 'poster', 'meeting')
    fields = ('rate', 'name', 'poster', 'meeting')

    def has_add_permission(self, request):
        return False


class PosterOptionInline(admin.TabularInline):
    model = PosterOption
    extra = 1


class MeetingOptionInline(admin.TabularInline):
    model = MeetingOption
    extra = 1


class WorkshopAdmin(markdownx.admin.MarkdownxModelAdmin):
    inlines = [RateInline, MeetingOptionInline, PosterOptionInline, InstructorInline]
    prepopulated_fields = {'slug': ('title', 'start_date')}
    list_display = ('dedicated_qiime2', 'title', 'start_date', 'end_date',
                    'live', 'is_open', 'total_tickets_sold',
                    'per_rate_tickets', 'charged')
    list_display_links = ('title', 'start_date', 'end_date')

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

    def is_open(self, obj):
        return obj.is_open
    is_open.boolean = True
    is_open.short_description = 'Sales Open?'

    def per_rate_tickets(self, obj):
        available_rates = obj.rate_set.filter(sold_out=False, sales_open=True)
        available = format_html_join('\n', '<li>{} ({}/{})</li>',
                                     ((r.name, r.ticket_count, r.capacity)
                                      for r in available_rates))
        sold_out_rates = obj.rate_set.filter(sold_out=True)
        sold_out = format_html_join('\n', '<li>{} ({}/{})</li>',
                                    ((r.name, r.ticket_count, r.capacity)
                                     for r in sold_out_rates))
        closed_rates = obj.rate_set.filter(sales_open=False)
        closed = format_html_join('\n', '<li>{} ({}/{})</li>',
                                  ((r.name, r.ticket_count, r.capacity)
                                   for r in closed_rates))
        if available == '' and sold_out == '' and closed == '':
            return '-'
        available = available if available != '' else 'No available rates'
        sold_out = sold_out if sold_out != '' else 'No sold out rates'
        closed = closed if closed != '' else 'No closed rates'
        return format_html('<span>Available</span><ul>{}</ul><span>Sold Out'
                           '</span><ul>{}</ul> <span>Closed</span><ul>{}</ul>',
                           available, sold_out, closed)
    per_rate_tickets.description = 'Per-rate Tickets'

    def charged(self, obj):
        charged = 0
        for rate in obj.rate_set.all():
            for order_item in rate.orderitem_set.all():
                if (order_item.order.billed_total != '' and
                        order_item.order.refunded is False):
                    charged += order_item.rate.price
        return '$%s' % charged


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('contact_name', 'contact_email', 'tickets', 'order_total',
                    'paid', 'refunded', 'order_datetime', 'billed_datetime',
                    'transaction_id')
    list_display_links = ('contact_name', 'contact_email')
    list_filter = (OrderWorkshopListFilter, OrderPaidListFilter,
                   OrderRefundedListFilter, 'order_datetime', 'contact_email')

    def paid(self, obj):
        return obj.billed_total != ''
    paid.admin_order_field = 'billed_total'
    paid.boolean = True

    def tickets(self, obj):
        return obj.orderitem_set.count()

    def has_add_permission(self, request):
        return False


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'workshop', 'rate', 'poster', 'meeting',
                    'paid', 'refunded', 'order_transaction_id')
    list_filter = (OrderItemWorkshopListFilter, OrderItemPaidListFilter,
                   OrderItemRefundedListFilter)

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


class InstructorAdmin(admin.ModelAdmin):
    # This hides `Instructors` on the admin changelist page
    def get_model_perms(self, request):
        return {}


admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
