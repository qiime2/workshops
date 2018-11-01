# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0031_workshop_dedicated_qiime2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='discount_code',
            field=models.SlugField(
                blank=True, help_text=(
                    'This will be the code given to a customer receiving a '
                    'discount in the form of https://workshops.qiime2.org/'
                    'workshop_slug/rate=discount_code')),
        ),
    ]
