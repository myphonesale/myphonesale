# Generated by Django 2.2 on 2020-04-30 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_auto_20200420_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.CharField(default='active', max_length=100),
        ),
    ]
