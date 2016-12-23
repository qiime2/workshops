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
        ('payments', '0027_rename_rate_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='sales_open',
            field=models.BooleanField(default=True),
        ),
    ]
