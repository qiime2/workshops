# Generated by Django 2.1.15 on 2020-09-15 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_add_ticket_help_prose'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='max_order',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
    ]
