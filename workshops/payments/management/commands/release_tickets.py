from django.core.management.base import BaseCommand
from django.db import transaction

from workshops.payments.models import Workshop, Rate


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('workshop_id', type=int)
        parser.add_argument('rate_id', type=int)
        parser.add_argument('tickets_to_add', type=int)

    def handle(self, *args, **options):
        workshop_id = options['workshop_id']
        rate_id = options['rate_id']
        tickets_to_add = options['tickets_to_add']

        workshop = Workshop.objects.get(id=workshop_id)
        rate = Rate.objects.get(id=rate_id)
        private_rates = Rate.objects.filter(private=True, parent=rate,
                                            sold_out=False, sales_open=False)

        with transaction.atomic():
            for private_rate in private_rates:
                private_rate.sales_open = True
                private_rate.save()

            rate.capacity = rate.capacity + tickets_to_add
            rate.save()
