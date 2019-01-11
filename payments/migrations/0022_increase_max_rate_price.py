# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0021_private_rates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='price (USD)'),
        ),
    ]
