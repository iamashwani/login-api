# Generated by Django 4.0.3 on 2022-04-18 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0024_alter_transcations_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcations',
            name='description',
            field=models.CharField(blank=True, default=1, max_length=200),
            preserve_default=False,
        ),
    ]