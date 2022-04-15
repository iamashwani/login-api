# Generated by Django 4.0.3 on 2022-04-12 06:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0011_alter_user_mobile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='deduct_amount',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='total_add_amount',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='total_win_amount',
        ),
        migrations.AddField(
            model_name='wallet',
            name='deposit_cash',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Full Add amount'),
        ),
        migrations.AddField(
            model_name='wallet',
            name='winning_cash',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='wallet',
            name='withdraw_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message='Mobile incorrect.', regex='^\\+?1?\\d{6,15}$')]),
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
        migrations.AlterField(
            model_name='wallet',
            name='add_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Add amount'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=10, verbose_name='Total amount'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='win_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]