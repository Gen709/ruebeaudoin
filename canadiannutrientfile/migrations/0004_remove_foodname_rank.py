# Generated by Django 4.0.5 on 2023-01-15 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('canadiannutrientfile', '0003_foodname_rank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodname',
            name='rank',
        ),
    ]
