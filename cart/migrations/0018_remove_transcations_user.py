# Generated by Django 4.0.3 on 2022-04-17 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0017_transcations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transcations',
            name='user',
        ),
    ]