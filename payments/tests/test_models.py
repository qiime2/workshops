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
        oi = OrderItemFactory()  # Create single ticket
        o, w = oi.order, oi.rate.workshop

        self.assertEqual(0, w.total_tickets_sold)

        o.billed_total = '100.00'  # Any non-empty string for now
        o.save()

        self.assertEqual(1, w.total_tickets_sold)

    def test_is_at_capacity(self):
        oi = OrderItemFactory()
        o, r, w = oi.order, oi.rate, oi.rate.workshop

        o.billed_total, w.capacity, r.capacity = 'asdf', 5, 5

        for m in [o, r, w]:
            m.save()

        self.assertEqual(False, w.is_at_capacity)
