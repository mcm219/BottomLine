# Generated by Django 3.2.2 on 2021-07-04 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blweb', '0007_vehicleconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicleconfig',
            name='config_name',
            field=models.CharField(blank=True, default=None, help_text='The name of this vehicle configuration', max_length=200, null=True),
        ),
    ]
