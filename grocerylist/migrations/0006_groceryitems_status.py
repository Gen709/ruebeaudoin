# Generated by Django 4.0.5 on 2023-01-15 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grocerylist', '0005_alter_groceryitems_qty'),
    ]

    operations = [
        migrations.AddField(
            model_name='groceryitems',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='grocerylist.groceryitemstatus'),
        ),
    ]