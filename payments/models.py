from django.db import models


class Workshop(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    url = models.URLField(max_length=2000)
    slug = models.SlugField()

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
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return '%s: %s' % (self.name, self.price)


class Order(models.Model):
    email = models.EmailField()
    order_total = models.DecimalField(max_digits=7, decimal_places=2)
    order_datetime = models.DateTimeField(auto_now_add=True)
    billed_total = models.DecimalField(max_digits=7, decimal_places=2,
                                       null=True)
    billed_datetime = models.DateTimeField(null=True)

    def __str__(self):
        return '%s: $%s on %s' % (self.email, self.order_total,
                                  self.order_datetime)


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    rate = models.ForeignKey(Rate)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.quantity)
