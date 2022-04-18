# Generated by Django 4.0.3 on 2022-04-18 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0017_alter_user_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transcations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=10, max_digits=10, verbose_name='amount')),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.wallet')),
            ],
        ),
    ]
