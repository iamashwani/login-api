# Generated by Django 4.0.3 on 2022-04-08 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_remove_user_user_id_alter_wallet_total_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='logo',
            new_name='profile_url',
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_id',
            field=models.IntegerField(default=0),
        ),
    ]