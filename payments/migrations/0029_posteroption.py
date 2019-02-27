# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0028_rate_sales_open'),
    ]

    operations = [
        migrations.CreateModel(
            name='PosterOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('sort_order', models.IntegerField(
                    help_text=('This value is used to sort the display order '
                               'of the poster presentation options'))),
                ('workshop', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='payments.Workshop')),
            ],
            options={
                'ordering': ('sort_order',),
            },
        ),
        migrations.AddField(
            model_name='orderitem',
            name='poster',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE,
                to='payments.PosterOption'),
        ),
    ]
