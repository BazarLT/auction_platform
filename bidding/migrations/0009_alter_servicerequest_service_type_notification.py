# Generated by Django 5.1.4 on 2024-12-22 14:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0008_remove_job_poster_delete_order_remove_bid_role_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicerequest',
            name='service_type',
            field=models.CharField(choices=[('mūrininkas', 'Mūrininkas'), ('elektrikas', 'Elektrikas'), ('darbininkas', 'Darbininkas'), ('dažytojas_dekoratorius', 'Dažytojas Dekoratorius'), ('santechnikas', 'Santechnikas'), ('mechanikas', 'Mechanikas'), ('buhalterinė_apskaita', 'Buhalterinė Apskaita'), ('IT_programuotojas', 'IT Programuotojas'), ('technikas', 'Technikas'), ('kitos_uzduotys', 'Kitos Užduotys')], max_length=50),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bidding.userprofile')),
            ],
        ),
    ]