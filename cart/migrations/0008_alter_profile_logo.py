# Generated by Django 4.0.3 on 2022-03-26 09:11

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_alter_profile_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='logo',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\admin\\Desktop\\api_basic\\login-api\\media'), upload_to='profile/'),
        ),
    ]
