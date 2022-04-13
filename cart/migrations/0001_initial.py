# Generated by Django 4.0.3 on 2022-04-13 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=20)),
                ('otp', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='profile/')),
                ('profile_dp', models.ImageField(blank=True, null=True, upload_to='profile/')),
                ('profile_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, default=10, max_digits=10, verbose_name='Total amount')),
                ('add_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Add amount')),
                ('deposit_cash', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Full Add amount')),
                ('win_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('winning_cash', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('withdraw_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wallet_mobile', to='cart.user')),
            ],
        ),
    ]
