# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payments', '0019_markdownx'),
    ]

    def migrate(apps, schema_editor):
        Workshop = apps.get_model('payments', 'Workshop')
        for row in Workshop.objects.all():
            row.private_code = uuid.uuid4()
            row.save()

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='private_code',
            field=models.SlugField(default=uuid.uuid4, help_text='This will be the unlock code for your private workshop: https://workshops.qiime.org/?code=<span id="pcode"></span>', max_length=300),
        ),
        migrations.RunPython(migrate, reverse_code=migrations.RunPython.noop),
        migrations.AddField(
            model_name='workshop',
            name='public',
            field=models.BooleanField(default=True, help_text='Private workshops will require a custom URL and will not be visible on the default Workshop List'),
        ),
        migrations.AlterUniqueTogether(
            name='workshop',
            unique_together=set([('private_code', 'public'), ('title', 'slug')]),
        ),
    ]
