# Generated by Django 2.2 on 2020-04-20 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_auto_20200420_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='final_price',
            field=models.CharField(default='0', max_length=100),
        ),
    ]
