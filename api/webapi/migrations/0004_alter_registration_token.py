# Generated by Django 3.2.7 on 2021-09-27 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0003_inputdata_temperature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='token',
            field=models.CharField(max_length=255),
        ),
    ]
