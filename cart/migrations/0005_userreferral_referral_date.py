# Generated by Django 4.0.3 on 2022-04-26 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_remove_user_referral_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userreferral',
            name='referral_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
