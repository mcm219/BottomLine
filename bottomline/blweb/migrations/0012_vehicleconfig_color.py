# Generated by Django 3.2.2 on 2021-07-10 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blweb', '0011_vehiclecolor'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicleconfig',
            name='color',
            field=models.ForeignKey(blank=True, default=None, help_text='The chosen color for this config', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='color', to='blweb.vehiclecolor'),
        ),
    ]
