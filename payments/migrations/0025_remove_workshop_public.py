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
        ('payments', '0024_remove_workshop_capacity'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='workshop',
            unique_together=set([('title', 'slug')]),
        ),
        migrations.RemoveField(
            model_name='workshop',
            name='private_code',
        ),
        migrations.RemoveField(
            model_name='workshop',
            name='public',
        ),
    ]
