# Generated by Django 3.2.2 on 2021-06-05 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blweb', '0002_vehiclemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclemodel',
            name='make',
            field=models.ForeignKey(default=None, help_text='The vehicle make that this model is associated with', on_delete=django.db.models.deletion.CASCADE, to='blweb.vehiclemake'),
        ),
        migrations.CreateModel(
            name='VehicleOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the vehicle option', max_length=200)),
                ('description', models.TextField(help_text='A description of the option package and what features it includes')),
                ('price', models.IntegerField(help_text='The price for this option')),
                ('model', models.ForeignKey(default=None, help_text='The vehicle model associated with this option package', on_delete=django.db.models.deletion.CASCADE, to='blweb.vehiclemodel')),
            ],
        ),
    ]