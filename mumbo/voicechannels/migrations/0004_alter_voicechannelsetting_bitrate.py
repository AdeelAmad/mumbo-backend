# Generated by Django 4.0.4 on 2022-04-25 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voicechannels', '0003_rename_voicechannelsettings_voicechannelsetting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voicechannelsetting',
            name='bitrate',
            field=models.IntegerField(default=64),
        ),
    ]
