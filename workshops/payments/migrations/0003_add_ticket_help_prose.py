# ----------------------------------------------------------------------------
# Copyright (c) 2016-2022, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

# Generated by Django 2.1.7 on 2019-03-15 23:12

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_byod_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='inline_purchase_instructions',
            field=markdownx.models.MarkdownxField(blank=True, help_text='This is the text that is rendered on the per-ticket sale page. Use this field to provide additional instructions. Supports Markdown.'),
        ),
    ]
