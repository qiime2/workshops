# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0023_order_refunded'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshop',
            name='capacity',
        ),
    ]
