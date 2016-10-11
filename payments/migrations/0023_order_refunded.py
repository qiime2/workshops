from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0022_increase_max_rate_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='refunded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='rate',
            name='discount_code',
            field=models.SlugField(blank=True, help_text='This will be the code given to a customer receiving a discount in the form of https://workshops.qiime.org/workshop_slug/rate=discount_code'),
        ),
    ]
