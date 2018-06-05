# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0018_workshops_defaults'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='description',
            field=markdownx.models.MarkdownxField(),
        ),
    ]
