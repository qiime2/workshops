# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import uuid

from django.db import models
from django.db.models.expressions import F
from django.core.exceptions import ValidationError

from subdomains.utils import reverse

from markdownx.models import MarkdownxField


class Workshop(models.Model):
    title = models.CharField(max_length=300)
    location = models.CharField(max_length=300)
    description = MarkdownxField()
    start_date = models.DateField()
    end_date = models.DateField()
    url = models.URLField(verbose_name='URL', max_length=2000, blank=True)
    slug = models.SlugField(help_text='This is the unique identifier for the '
                            'URL (i.e. title-YYYY-MM-DD)')
    draft = models.BooleanField(help_text='Draft workshops do not show up on '
                                'the workshop list overview', default=True)
    capacity = models.PositiveIntegerField()
    sales_open = models.BooleanField(help_text='Closed workshops do not show '
                                     'up on the workshop list overview',
                                     default=False)
    public = models.BooleanField(help_text='Private workshops will require a '
                                 'custom URL and will not be visible on the '
                                 'default Workshop List', default=True)
    # SlugField will provide the correct sanitization for URL safe values
    private_code = models.SlugField(help_text='This will be the unlock code '
                                    'for your private workshop: https://work'
                                    'shops.qiime.org/?code=<span id="pcode">'
                                    '</span>', default=uuid.uuid4,
                                    max_length=300)

    @property
    def total_tickets_sold(self):
        return OrderItem.objects.filter(rate__workshop=self) \
                .exclude(order__billed_total='').count()

    @property
    def is_at_capacity(self):
        return self.total_tickets_sold >= self.capacity

    @property
    def is_open(self):
        if self.sales_open:
            return not self.is_at_capacity
        return self.sales_open

    @property
    def available_rates(self):
        return self.rate_set.filter(sold_out=False)

    @property
    def sold_out_rates(self):
        return self.rate_set.filter(sold_out=True)

    class Meta:
        unique_together = (('title', 'slug'), ('private_code', 'public'))

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
        return reverse('payments:details', kwargs={'slug': self.slug},
                       subdomain='workshops')

    def filter_rates(self, rate_code):
        rate_set = None
        if rate_code:
            rate_set = self.rate_set.filter(discount_code=rate_code)\
                .order_by('price')

        if rate_code is None or len(rate_set) == 0:
            rate_set = self.rate_set.filter(discount=False).order_by('price')
        return rate_set


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
            .annotate(ticket_count=models.Count('orderitem')) \
            .annotate(sold_out=models.Case(
                          models.When(
                              ticket_count__lt=F('capacity'),
                              then=models.Value(False),
                          ),
                          default=True,
                          output_field=models.BooleanField(),
                        ))


class Rate(models.Model):
    workshop = models.ForeignKey(Workshop)
    name = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=8, decimal_places=2,
                                verbose_name='price (USD)')
    capacity = models.PositiveIntegerField()
    discount = models.BooleanField(default=False)
    discount_code = models.SlugField(help_text='This will be the code given to'
                                     ' a customer receiving a discount in the '
                                     'form of https://workshops.qiime.org/wor'
                                     'kshop_slug/rate=discount_code',
                                     blank=True)
    objects = RateManager()

    def clean(self):
        # assign a UUID if it is a discount, but no custom code was given
        if self.discount and not self.discount_code:
            self.discount_code = uuid.uuid4()
        return super().clean()

    def __str__(self):
        return '%s: $%s' % (self.name, self.price)


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

    def __str__(self):
        return '%s: $%s on %s' % (self.contact_email, self.order_total,
                                  self.order_datetime)


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    rate = models.ForeignKey(Rate)
    email = models.EmailField()
    name = models.CharField(max_length=500)

    def __str__(self):
        return str(self.email)

    class Meta:
        unique_together = (('order', 'rate', 'email'), )
