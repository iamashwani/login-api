# Generated by Django 4.0.3 on 2022-04-19 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0030_wallet_referral_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='Bonus',
            field=models.FloatField(default=0),
        ),
    ]