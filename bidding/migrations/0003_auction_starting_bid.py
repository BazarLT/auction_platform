# Generated by Django 5.1.3 on 2024-11-24 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0002_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, default=12.18, max_digits=10),
            preserve_default=False,
        ),
    ]
