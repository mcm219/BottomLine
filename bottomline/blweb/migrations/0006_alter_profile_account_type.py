# Generated by Django 3.2.2 on 2021-06-20 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blweb', '0005_alter_profile_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account_type',
            field=models.IntegerField(default=1, help_text='The type of account (dealer or shopper)'),
        ),
    ]
