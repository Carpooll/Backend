# Generated by Django 3.2.4 on 2021-07-19 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_coordinate_y'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='coordinate_x',
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name='profile',
            name='coordinate_y',
            field=models.FloatField(default=None),
        ),
    ]
