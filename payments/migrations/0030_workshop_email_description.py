# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0029_posteroption'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='email_description',
            field=markdownx.models.MarkdownxField(blank=True, help_text='This is the text that is emailed to all workshop attendees when their payment is processed. Supports Markdown.'),
        ),
    ]
