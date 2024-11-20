# bidding/migrations/0002_rename_start_bid_auction_starting_bid_and_more.py

from django.db import migrations, models
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='start_bid',
            new_name='starting_bid',
        ),
        migrations.RemoveField(
            model_name='auction',
            name='end_date',
        ),
        migrations.AddField(
            model_name='auction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 11, 14, 0, 0)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auction',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='auction',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='Bid',
        ),
    ]
