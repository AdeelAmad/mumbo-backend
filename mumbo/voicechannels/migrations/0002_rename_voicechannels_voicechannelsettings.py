# Generated by Django 4.0.4 on 2022-04-25 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_alter_guild_id'),
        ('voicechannels', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='voicechannels',
            new_name='voicechannelsettings',
        ),
    ]