# Generated by Django 4.0.3 on 2022-04-07 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wallet',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=10, verbose_name='total amount'),
        ),
    ]
