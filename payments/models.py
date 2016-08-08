import uuid
from datetime import date

from django.db import models
from django.core.exceptions import ValidationError


class Workshop(models.Model):
    title = models.CharField(max_length=300)
    location = models.CharField(max_length=300)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    closing_date = models.DateField()
    url = models.URLField(verbose_name='URL', max_length=2000)
    slug = models.SlugField(help_text='This is the unique identifier for the '
                            'URL (i.e. title-YYYY-MM-DD)')

    @property
    def is_open(self):
        return self.closing_date >= date.today()

    class Meta:
        unique_together = (('title', 'slug'), )

    def clean(self):
        # Make sure the workshop closes before it starts...
        if self.closing_date > self.start_date:
            raise ValidationError('A Workshop\'s closing date must be before '
                                  'the start date.')
        # Make sure the workshop begins before it can end...
        if self.start_date > self.end_date:
            raise ValidationError('A Workshop\'s start date must be before '
                                  'the end date.')
        return super().clean()

    def __str__(self):
        return self.title


class Instructor(models.Model):
    name = models.CharField(max_length=300)
    workshops = models.ManyToManyField(Workshop, related_name='instructors')

    def __str__(self):
        return self.name


class Rate(models.Model):
    workshop = models.ForeignKey(Workshop)
    name = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                verbose_name='price (USD)')

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

    def __str__(self):
        return str(self.email)

    class Meta:
        unique_together = (('order', 'rate', 'email'), )
