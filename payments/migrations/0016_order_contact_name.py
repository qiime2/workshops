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
        ('payments', '0015_order_datetime_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='contact_name',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]
