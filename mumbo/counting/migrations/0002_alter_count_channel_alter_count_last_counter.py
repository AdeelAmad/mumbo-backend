# Generated by Django 4.0.4 on 2022-04-24 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='count',
            name='channel',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='count',
            name='last_counter',
            field=models.IntegerField(),
        ),
    ]
