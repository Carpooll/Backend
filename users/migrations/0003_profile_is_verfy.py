# Generated by Django 3.2.4 on 2021-07-18 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210718_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_verfy',
            field=models.BooleanField(default=False),
        ),
    ]
