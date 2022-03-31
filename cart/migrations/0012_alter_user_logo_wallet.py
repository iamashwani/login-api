# Generated by Django 4.0.3 on 2022-03-31 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0011_rename_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='logo',
            field=models.ImageField(blank=True, default='image.jpg', null=True, upload_to='profile/'),
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='total')),
                ('add_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='amount')),
                ('win_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('deduct_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.user')),
            ],
        ),
    ]