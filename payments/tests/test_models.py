# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.test import TestCase

from .factories import WorkshopFactory, OrderItemFactory
from ..models import Workshop


class WorkshopTestCase(TestCase):
    def test_creation(self):
        w = WorkshopFactory()
        self.assertTrue(isinstance(w, Workshop))
        self.assertEqual(str(w), w.title)

    def test_total_tickets_sold(self):
        # Create a single order item (ticket)
        oi = OrderItemFactory(order__billed_total='100.00')
        self.assertEqual(1, oi.rate.workshop.total_tickets_sold)

        oi = OrderItemFactory(order__billed_total='')
        self.assertEqual(0, oi.rate.workshop.total_tickets_sold)

    def test_is_at_capacity(self):
        oi = OrderItemFactory(order__billed_total='asdf', rate__capacity=5,
                              rate__workshop__capacity=5)
        self.assertEqual(False, oi.rate.workshop.is_at_capacity)
