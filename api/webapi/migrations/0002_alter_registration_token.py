# Generated by Django 3.2.7 on 2021-09-22 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='token',
            field=models.CharField(max_length=162),
        ),
    ]
