# Generated by Django 4.1.4 on 2022-12-22 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inertiatools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=100)),
            ],
        ),
    ]
