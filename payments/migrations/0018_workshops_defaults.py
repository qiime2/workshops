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
        ('payments', '0017_billed_total_charfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='draft',
            field=models.BooleanField(default=True, help_text='Draft workshops do not show up on the workshop list overview'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='sales_open',
            field=models.BooleanField(default=False, help_text='Closed workshops do not show up on the workshop list overview'),
        ),
    ]
