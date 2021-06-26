# Generated by Django 3.2.2 on 2021-06-20 17:34

import blweb.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blweb', '0004_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account_type',
            field=models.IntegerField(default=blweb.models.AccountType['SHOPPER'], help_text='The type of account (dealer or shopper)'),
        ),
    ]
