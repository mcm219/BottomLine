# Generated by Django 3.2.2 on 2021-07-14 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blweb', '0012_vehicleconfig_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclemodel',
            name='price',
            field=models.IntegerField(default=0, help_text='The base MSRP for the model, not including options'),
        ),
    ]
