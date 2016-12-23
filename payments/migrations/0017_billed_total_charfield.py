# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0016_order_contact_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='billed_total',
            field=models.CharField(blank=True, default='', help_text='This is the confirmed paid amount from NAU', max_length=300, verbose_name='billed total (USD)'),
            preserve_default=False,
        ),
    ]
