# Generated by Django 4.0.4 on 2022-04-24 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counting', '0003_alter_count_channel_alter_count_last_counter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='count',
            name='channel',
            field=models.TextField(default=None, max_length=18),
        ),
        migrations.AlterField(
            model_name='count',
            name='last_count',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='count',
            name='last_counter',
            field=models.TextField(default=None, max_length=18),
        ),
    ]
