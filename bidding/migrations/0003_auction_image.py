# Generated by Django 5.1.3 on 2024-12-07 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0002_order_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='auctions/'),
        ),
    ]
