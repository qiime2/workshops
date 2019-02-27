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
        ('payments', '0022_increase_max_rate_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='refunded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='rate',
            name='discount_code',
            field=models.SlugField(
                blank=True, help_text=('This will be the code given to a '
                                       'customer receiving a discount in the '
                                       'form of https://workshops.qiime.org/wo'
                                       'rkshop_slug/rate=discount_code')),
        ),
    ]
