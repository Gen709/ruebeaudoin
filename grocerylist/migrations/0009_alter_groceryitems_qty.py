# Generated by Django 4.0.5 on 2023-01-17 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocerylist', '0008_alter_groceryitems_price_alter_groceryitems_qty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groceryitems',
            name='qty',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
