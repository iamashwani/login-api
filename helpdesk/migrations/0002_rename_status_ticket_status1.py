# Generated by Django 4.0.3 on 2022-04-27 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='status',
            new_name='status1',
        ),
    ]