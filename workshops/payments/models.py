import uuid

from django.urls import reverse
from django.db import models
from django.db.models.expressions import F
from django.core.exceptions import ValidationError


from markdownx.models import MarkdownxField


class Workshop(models.Model):
    title = models.CharField(max_length=300)
    dedicated_qiime2 = models.BooleanField(default=False)
    location = models.CharField(max_length=300)
    description = MarkdownxField()
    email_description = MarkdownxField(help_text='This is the text that is '
                                       'emailed to all workshop attendees '
                                       'when their payment is processed. '
                                       'Supports Markdown.',
                                       blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    url = models.URLField(verbose_name='URL', max_length=2000, blank=True)
    slug = models.SlugField(help_text='This is the unique identifier for the '
                            'URL (i.e. title-YYYY-MM-DD)')
    draft = models.BooleanField(help_text='Draft workshops do not show up on '
                                'the workshop list overview', default=True)
    inline_purchase_instructions = MarkdownxField(help_text='This is the text '
                                                  'that is rendered on the '
                                                  'per-ticket sale page. Use '
                                                  'this field to provide '
                                                  'additional instructions. '
                                                  'Supports Markdown.',
                                                  blank=True)

    @property
    def total_tickets_sold(self):
        return OrderItem.objects.filter(rate__workshop=self) \
                .exclude(order__billed_total='') \
                .exclude(order__refunded=True).count()

    @property
    def is_open(self):
        return self.rate_set.filter(private=False, sold_out=False,
                                    sales_open=True).count() != 0

    @property
    def available_rates(self):
        return self.rate_set.filter(sold_out=False)

    @property
    def sold_out_rates(self):
        return self.rate_set.filter(sold_out=True)

    class Meta:
        unique_together = (('title', 'slug'),)

    def clean(self):
        # Make sure the workshop begins before it can end...
        if self.start_date > self.end_date:
            raise ValidationError('A Workshop\'s start date must be before '
                                  'the end date.')
        return super().clean()

    def __str__(self):
        return self.title

    # For django admin 'view on site' link
    def get_absolute_url(self):
        return reverse('payments:details', kwargs={'slug': self.slug})

    def filter_rates(self, rate_code):
        rate_set = None
        if rate_code:
            rate_set = self.rate_set.filter(
                discount_code=rate_code, sales_open=True).order_by('price')

        if rate_code is None or len(rate_set) == 0:
            rate_set = self.rate_set.filter(
                private=False, sales_open=True).order_by('price')
        return rate_set.all()


class Instructor(models.Model):
    name = models.CharField(max_length=300)
    # Allow blanks otherwise workshops are needed to be assigned upon creation
    workshops = models.ManyToManyField(Workshop, related_name='instructors',
                                       blank=True)

    def __str__(self):
        return self.name


class RateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .annotate(ticket_count=models.Sum(
                models.Case(
                    models.When(
                        orderitem__order__refunded=True,
                        then=0
                    ),
                    models.When(
                        orderitem__order__billed_total='',
                        then=0
                    ),
                    models.When(
                        orderitem__order__billed_total__isnull=True,
                        then=0
                    ),
                    default=1,
                    output_field=models.IntegerField(),
                ))) \
            .annotate(sold_out=models.Case(
                          models.When(
                              ticket_count__lt=F('capacity'),
                              then=models.Value(False),
                          ),
                          default=True,
                          output_field=models.BooleanField(),
                        ))


class PosterOption(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    sort_order = models.IntegerField(help_text='This value is used to sort '
                                     'the display order of the poster '
                                     'presentation options')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('sort_order',)


class MeetingOption(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    sort_order = models.IntegerField(help_text='This value is used to sort '
                                     'the display order of the BYOD '
                                     'meeting options')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('sort_order',)


class Rate(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=8, decimal_places=2,
                                verbose_name='price (USD)')
    max_order = models.PositiveIntegerField(null=True, default=None, blank=True)
    capacity = models.PositiveIntegerField()
    private = models.BooleanField(default=False)
    discount_code = models.SlugField(help_text='This will be the code given to'
                                     ' a customer receiving a discount in the '
                                     'form of https://workshops.qiime2.org/wor'
                                     'kshop_slug/rate=discount_code',
                                     blank=True)
    sales_open = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None,
                               null=True, blank=True)

    objects = RateManager()

    def clean(self):
        # assign a UUID if it is a discount, but no custom code was given
        if self.private:
            if not self.discount_code:
                self.discount_code = uuid.uuid4()
            else:
                res = Rate.objects.filter(discount_code=self.discount_code)
                if len(res) > 0 and self not in res:
                    raise ValidationError(
                        'Discount codes must be unique. The code %s on the %s '
                        'is already in use.' % (self.discount_code, self)
                    )

        return super().clean()

    def __str__(self):
        return '%s %s: %s ($%s)' % (self.workshop.id, self.workshop.title, self.name, self.price)


class Order(models.Model):
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False)
    contact_name = models.CharField(max_length=300)
    contact_email = models.EmailField()
    order_total = models.DecimalField(max_digits=7, decimal_places=2,
                                      verbose_name='order total (USD)')
    order_datetime = models.DateTimeField(auto_now_add=True)
    billed_total = models.CharField(
        blank=True,
        max_length=300,
        verbose_name='billed total (USD)',
        help_text='This is the confirmed paid amount from NAU'
    )
    billed_datetime = models.CharField(
        blank=True,
        max_length=300,
        help_text='This is the confirmed date and time of payment',
        verbose_name='billed date & time'
    )
    refunded = models.BooleanField(default=False)

    def __str__(self):
        return '%s: $%s on %s' % (self.contact_email, self.order_total,
                                  self.order_datetime)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE)
    poster = models.ForeignKey(PosterOption, null=True, on_delete=models.CASCADE)
    meeting = models.ForeignKey(MeetingOption, null=True, on_delete=models.CASCADE)
    email = models.EmailField()
    name = models.CharField(max_length=500)

    def __str__(self):
        return str(self.email)

    class Meta:
        unique_together = (('order', 'rate', 'email'), )
