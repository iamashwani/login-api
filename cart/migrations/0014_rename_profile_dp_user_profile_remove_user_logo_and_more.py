# Generated by Django 4.0.3 on 2022-04-14 18:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_rename_profile_user_logo_remove_user_profile_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='profile_dp',
            new_name='profile',
        ),
        migrations.RemoveField(
            model_name='user',
            name='logo',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message='Mobile incorrect.', regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
