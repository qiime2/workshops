# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0030_workshop_email_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='dedicated_qiime2',
            field=models.BooleanField(default=False),
        ),
    ]
