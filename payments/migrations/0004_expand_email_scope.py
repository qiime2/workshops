# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_workshop_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='email',
            new_name='contact_email',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='email',
            field=models.EmailField(default='example@example.com',
                                    max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workshop',
            name='closing_date',
            field=models.DateField(
                default=datetime.datetime(2016, 8, 7, 23, 54, 27, 693604,
                                          tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='orderitem',
            unique_together=set([('order', 'rate', 'email')]),
        ),
        migrations.AlterUniqueTogether(
            name='workshop',
            unique_together=set([('title', 'slug')]),
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='quantity',
        ),
    ]
