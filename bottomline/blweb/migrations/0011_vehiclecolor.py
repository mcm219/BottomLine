# Generated by Django 3.2.2 on 2021-07-06 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blweb', '0010_alter_vehicleconfig_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleColor',
            fields=[
                ('vehicleoption_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blweb.vehicleoption')),
            ],
            bases=('blweb.vehicleoption',),
        ),
    ]