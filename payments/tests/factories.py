# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import datetime

import factory
from factory.fuzzy import (FuzzyDate, FuzzyText, FuzzyChoice, FuzzyDecimal,
                           FuzzyInteger)

from ..models import Instructor, Rate, Workshop, Order, OrderItem


class WorkshopFactory(factory.DjangoModelFactory):
    class Meta:
        model = Workshop

    title = FuzzyText(length=50)
    location = FuzzyText(length=50)
    description = FuzzyText(length=50)
    start_date = FuzzyDate(datetime.date(2016, 1, 1),
                           datetime.date(2016, 12, 31))
    end_date = FuzzyDate(datetime.date(2017, 1, 1),
                         datetime.date(2017, 12, 31))
    url = factory.LazyAttribute(lambda o: '%s.com' % o.title)
    slug = factory.Sequence(lambda n: 'workshop%d' % n)
    draft = FuzzyChoice([True, False])
    capacity = FuzzyInteger(1, 100)
    sales_open = FuzzyChoice([True, False])


class InstructorFactory(factory.DjangoModelFactory):
    class Meta:
        model = Instructor

    name = FuzzyText(length=50)
    workshop = factory.SubFactory(WorkshopFactory)


class RateFactory(factory.DjangoModelFactory):
    class Meta:
        model = Rate

    workshop = factory.SubFactory(WorkshopFactory)
    name = FuzzyText(length=50)
    price = FuzzyDecimal(0.5, 1000.0)
    capacity = FuzzyInteger(1, 100)


class OrderFactory(factory.DjangoModelFactory):
    class Meta:
        model = Order

    contact_name = FuzzyText(length=50)
    contact_email = FuzzyText(length=50)
    order_total = FuzzyDecimal(0.50, 1000.00)


class OrderItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    rate = factory.SubFactory(RateFactory)
    name = FuzzyText(length=50)
    email = FuzzyText(length=50)
