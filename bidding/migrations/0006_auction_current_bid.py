# Generated by Django 5.1.3 on 2024-12-01 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0005_servicerequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='current_bid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
