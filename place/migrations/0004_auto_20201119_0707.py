# Generated by Django 3.1.3 on 2020-11-19 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0003_auto_20201119_0705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='region',
            field=models.CharField(default='서울', max_length=200),
        ),
        migrations.AlterField(
            model_name='place',
            name='title',
            field=models.CharField(default='이뻐요', max_length=100),
        ),
    ]
