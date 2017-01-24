# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError

from .factories import (WorkshopFactory, InstructorFactory, RateFactory,
                        OrderFactory, OrderItemFactory)
from ..models import Workshop, Instructor, Rate, Order, OrderItem


class WorkshopTestCase(TestCase):
    def test_creation(self):
        w = WorkshopFactory()
        self.assertTrue(isinstance(w, Workshop))
        self.assertEqual(str(w), w.title)

    def test_has_instructor(self):
        w = WorkshopFactory()
        i = InstructorFactory(workshops=[w])
        self.assertEqual(i.workshops.first(), w)

    def test_is_open(self):
        w = WorkshopFactory()
        self.assertFalse(w.is_open)
        [RateFactory(workshop=w) for i in range(5)]
        self.assertTrue(w.is_open)

    def test_has_available_rates(self):
        w = WorkshopFactory()
        [RateFactory(workshop=w) for i in range(5)]
        self.assertEqual(len(w.available_rates), 5)

    def test_has_sold_out_rates(self):
        w = WorkshopFactory()
        RateFactory(workshop=w, capacity=0)
        self.assertEqual(len(w.sold_out_rates), 1)

    def test_has_no_sold_out_rates(self):
        w = WorkshopFactory()
        [RateFactory(workshop=w) for i in range(5)]
        self.assertEqual(len(w.sold_out_rates), 0)

    def test_generates_proper_slug(self):
        slug = 'title-YYYY-MM-DD'
        w = WorkshopFactory(slug=slug)
        self.assertEqual(w.slug, slug)

    def test_generates_proper_url(self):
        slug = 'this-is-my-slug'
        url = 'http://workshops.example.com/%s/' % slug
        w = WorkshopFactory(slug=slug)
        self.assertEqual(w.get_absolute_url(), url)

    def test_catches_bad_dates(self):
        w = WorkshopFactory(
            start_date=datetime.date(2016, 8, 24),
            end_date=datetime.date(2016, 8, 23)
        )
        self.assertLess(w.end_date, w.start_date)
        # Because save doesn't use clean we have to call it directly
        self.assertRaises(ValidationError, w.clean)

    def test_allows_good_dates(self):
        w = WorkshopFactory(
            start_date=datetime.date(2016, 8, 23),
            end_date=datetime.date(2016, 8, 24)
        )
        self.assertLess(w.start_date, w.end_date)
        raised = False
        try:
            w.clean()
        except ValidationError:
            raised = True
        self.assertFalse(raised)


class InstructorTestCase(TestCase):
    def test_creation(self):
        i = InstructorFactory(workshops=[WorkshopFactory() for i in range(5)])
        self.assertEqual(len(i.workshops.all()), 5)
        self.assertTrue(isinstance(i, Instructor))
        self.assertEqual(str(i), i.name)


class RateTestCase(TestCase):
    def test_creation(self):
        r = RateFactory()
        self.assertTrue(isinstance(r, Rate))
        r_str = '%s: $%s' % (r.name, r.price)
        self.assertEqual(str(r), r_str)


class OrderTestCase(TestCase):
    def test_creation(self):
        o = OrderFactory()
        self.assertTrue(isinstance(o, Order))
        o_str = '%s: $%s on %s' % (o.contact_email, o.order_total,
                                   o.order_datetime)
        self.assertEqual(str(o), o_str)


class OrderItemTestCase(TestCase):
    def test_creation(self):
        oi = OrderItemFactory()
        self.assertTrue(isinstance(oi, OrderItem))
        self.assertEqual(str(oi), oi.email)

    def test_total_tickets_sold(self):
        # Create a single order item (ticket)
        oi = OrderItemFactory(order__billed_total='100.00')
        self.assertEqual(1, oi.rate.workshop.total_tickets_sold)

        oi = OrderItemFactory(order__billed_total='')
        self.assertEqual(0, oi.rate.workshop.total_tickets_sold)

    # def test_is_at_capacity(self):
    #     oi = OrderItemFactory(order__billed_total='asdf', rate__capacity=5,
    #                           rate__workshop__capacity=5)
    #     self.assertEqual(False, oi.rate.workshop.is_at_capacity)
