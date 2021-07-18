# Generated by Django 3.2.4 on 2021-07-18 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=50)),
                ('suburb', models.CharField(max_length=50)),
                ('postal_code', models.IntegerField()),
                ('internal_number', models.IntegerField(blank=True, null=True)),
                ('external_number', models.IntegerField()),
                ('coordinate_x', models.IntegerField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['created_at']},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='coordinate_x',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='external_number',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='internal_number',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='street',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='suburb',
        ),
        migrations.AddField(
            model_name='profile',
            name='adress',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.adress'),
        ),
    ]
