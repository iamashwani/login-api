# Generated by Django 4.0.3 on 2022-04-19 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0032_remove_wallet_bonus'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='Bonus',
            field=models.FloatField(default=0),
        ),
    ]