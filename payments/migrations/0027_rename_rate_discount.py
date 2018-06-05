# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0026_remove_workshop_sales_open'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rate',
            old_name='discount',
            new_name='private',
        ),
    ]
