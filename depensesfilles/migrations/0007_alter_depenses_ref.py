# Generated by Django 4.0.5 on 2023-03-08 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('depensesfilles', '0006_remove_depenses_categorie_1_depenses_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depenses',
            name='ref',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='bills'),
        ),
    ]
