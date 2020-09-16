import csv
import uuid

from django.core.management.base import BaseCommand
from django.db import transaction

from workshops.payments.models import Workshop, Rate


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('workshop_id', type=int)
        parser.add_argument('parent_rate_id', type=int)
        parser.add_argument('input_fp', type=str)
        parser.add_argument('output_fp', type=str)

    def handle(self, *args, **options):
        workshop_id = options['workshop_id']
        parent_rate_id = options['parent_rate_id']
        input_fp = options['input_fp']
        output_fp = options['output_fp']

        workshop = Workshop.objects.get(id=workshop_id)
        parent_rate = Rate.objects.get(id=parent_rate_id)

        with \
                open(input_fp) as fh_input, \
                open(output_fp, 'w') as fh_output, \
                transaction.atomic():
            reader = csv.reader(fh_input, delimiter=',')
            next(reader)  # skip header row

            for (email, price) in reader:
                rate, _ = Rate.objects.get_or_create(
                    workshop=workshop,
                    name='PPP: %s' % (email,),
                    price=price.strip('$'),
                    max_order=1,
                    capacity=1,
                    private=True,
                    sales_open=False,
                    parent=parent_rate,
                    discount_code=uuid.uuid4()
                )
                fh_output.write('%s,%s,%s\n' % (email, rate.price, rate.discount_code))
