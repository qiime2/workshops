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
    list_display = ('title', 'closing_date', 'start_date', 'end_date', 'url',
                    '_draft')

    def _draft(self, obj):
        return not obj.draft
    _draft.boolean = True
    _draft.short_description = 'Live?'


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


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ('contact_email', 'order_total', 'billed_total',
                       'billed_datetime', 'transaction_id')
    list_display = ('contact_email', 'order_total', 'order_datetime',
                    'billed_total', 'billed_datetime', 'transaction_id')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'rate', 'email')
    readonly_fields = ('order', 'rate', 'email')

admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Instructor)
admin.site.register(Rate, RateAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
