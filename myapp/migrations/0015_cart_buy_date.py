# Generated by Django 2.2 on 2020-05-01 09:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_cart_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='buy_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
