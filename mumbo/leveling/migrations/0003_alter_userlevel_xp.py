# Generated by Django 4.0.4 on 2022-05-04 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leveling', '0002_levelingsetting_levelupchannel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlevel',
            name='xp',
            field=models.BigIntegerField(default=0),
        ),
    ]
