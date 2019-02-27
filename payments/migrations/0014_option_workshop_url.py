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
        ('payments', '0013_workshop_sales_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='url',
            field=models.URLField(
                blank=True, max_length=2000, verbose_name='URL'),
        ),
    ]
