# Generated by Django 4.0.3 on 2022-04-12 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_rename_deduct_amount_wallet_withdraw_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='profile_id',
            new_name='profile_url',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_dp',
            field=models.ImageField(blank=True, null=True, upload_to='profile/'),
        ),
    ]
