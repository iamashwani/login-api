# Generated by Django 4.0.3 on 2022-04-19 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0031_wallet_bonus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='Bonus',
        ),
    ]