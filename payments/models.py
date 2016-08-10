import uuid
from datetime import date

from django.db import models
from django.db.models.expressions import F
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse


class Workshop(models.Model):
    title = models.CharField(max_length=300)
    location = models.CharField(max_length=300)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    url = models.URLField(verbose_name='URL', max_length=2000)
    slug = models.SlugField(help_text='This is the unique identifier for the '
                            'URL (i.e. title-YYYY-MM-DD)')
    draft = models.BooleanField(help_text='Draft workshops do not show up on '
                                'the workshop list overview')

    @property
    def is_open(self):
        return self.start_date >= date.today()

    @property
    def available_rates(self):
        return self.rate_set.filter(sold_out=False)

    @property
    def sold_out_rates(self):
        return self.rate_set.filter(sold_out=True)

    class Meta:
        unique_together = (('title', 'slug'), )

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
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                verbose_name='price (USD)')
    capacity = models.PositiveIntegerField()

    objects = RateManager()

    def __str__(self):
        return '%s: $%s' % (self.name, self.price)


class Order(models.Model):
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False)
    contact_email = models.EmailField()
    order_total = models.DecimalField(max_digits=7, decimal_places=2,
                                      verbose_name='order total (USD)')
    order_datetime = models.DateTimeField(auto_now_add=True)
    billed_total = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        verbose_name='billed total (USD)',
        help_text='This is the confirmed paid amount from NAU'
    )
    billed_datetime = models.DateTimeField(
        null=True,
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
