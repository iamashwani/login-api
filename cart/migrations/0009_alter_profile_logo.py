# Generated by Django 4.0.3 on 2022-03-26 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_alter_profile_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='logo',
            field=models.FileField(default='download (4).jpg', upload_to='profile/'),
        ),
    ]