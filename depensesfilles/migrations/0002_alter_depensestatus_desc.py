# Generated by Django 4.0.5 on 2022-07-13 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('depensesfilles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depensestatus',
            name='desc',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
