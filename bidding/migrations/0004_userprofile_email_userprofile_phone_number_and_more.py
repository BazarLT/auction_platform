# Generated by Django 5.1.3 on 2024-11-24 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0003_auction_starting_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('client', 'Client'), ('guest', 'Guest'), ('master', 'Master')], default='guest', max_length=6),
        ),
    ]
