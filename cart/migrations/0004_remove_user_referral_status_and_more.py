# Generated by Django 4.0.3 on 2022-04-26 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_remove_transaction_bonus_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='referral_status',
        ),
        migrations.RemoveField(
            model_name='userreferral',
            name='referral_resource',
        ),
    ]
