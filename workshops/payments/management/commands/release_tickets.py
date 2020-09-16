from django.core.management.base import BaseCommand
from django.db import transaction

from workshops.payments.models import Rate


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('rate_id', type=int)
        parser.add_argument('tickets_to_add', type=int)
        parser.add_argument('max_ticket_capacity', type=int)

    def handle(self, *args, **options):
        rate_id = options['rate_id']
        tickets_to_add = options['tickets_to_add']
        max_ticket_capacity = options['max_ticket_capacity']

        rate = Rate.objects.get(id=rate_id)
        private_rates = Rate.objects.filter(private=True, parent=rate,
                                            sold_out=False, sales_open=False)

        with transaction.atomic():
            for private_rate in private_rates:
                private_rate.sales_open = True
                private_rate.save()

            if rate.capacity + tickets_to_add < max_ticket_capacity:
                rate.capacity = rate.capacity + tickets_to_add
            else:
                rate.capacity = max_ticket_capacity
            rate.sales_open = True
            rate.save()
