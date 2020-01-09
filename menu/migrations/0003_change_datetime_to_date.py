"""Converts DateTimeFields to DateFields

1. Creates three temporary DateFields to back up DateTimeFields.
2. Alters DateTimeFields to allow null values and sets them to null.*
3. Alters DateTimeFields, converts them to DateFields, sets null back to False.
4. Loads the DateTimeFields' old values back in as dates.
5. Removes temporary DateFields.

* This is to prevent an error that will be thrown if Django tries to read
  a DateField with a leftover datetime value after the migration alters the
  field type. The SQLite API attempts to call convert_date, which splits
  the value on '-', casts each part to an int, and then uses the split parts
  to create a date object.

  If the value in the field is '2027-12-01 07:00:00', for example, the last
  part is '01 07:00:00', which causes a ValueError when convert_date attempts
  to cast to int.

  Without getting rid of the current value, the model's queryset can no longer
  be read without errors.
"""

from copy import copy
from datetime import date

from django.db import migrations, models


def set_temp_datefields(apps, schema_editor):
    """Converts current datetime to date and stores it in temporary field."""

    Menu = apps.get_model('menu', 'Menu')
    Item = apps.get_model('menu', 'Item')

    for menu in Menu.objects.all():
        menu.temp_created_date = menu.created_date.date()
        if menu.expiration_date:
            menu.temp_expiration_date = menu.expiration_date.date()
        menu.save()

    for item in Item.objects.all():
        item.temp_created_date = item.created_date.date()
        item.save()


def nullify_datetimefields(apps, schema_editor):
    """Sets value of DateTimeFields to None"""

    Menu = apps.get_model('menu', 'Menu')
    Item = apps.get_model('menu', 'Item')

    for menu in Menu.objects.all():
        menu.created_date = None
        menu.expiration_date = None
        menu.save()

    for item in Item.objects.all():
        item.created_date = None
        item.save()


def set_datefields_from_temp_datefields(apps, schema_editor):
    """Loads dates saved in temporary date fields into newly altered fields."""

    Menu = apps.get_model('menu', 'Menu')
    Item = apps.get_model('menu', 'Item')

    for menu in Menu.objects.all():
        menu.created_date = menu.temp_created_date
        menu.expiration_date = menu.temp_expiration_date
        menu.save()

    for item in Item.objects.all():
        item.created_date = item.temp_created_date
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20160406_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='temp_created_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='menu',
            name='temp_created_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='menu',
            name='temp_expiration_date',
            field=models.DateField(null=True),
        ),

        migrations.RunPython(set_temp_datefields),

        migrations.AlterField(
            model_name='item',
            name='created_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='created_date',
            field=models.DateTimeField(null=True),
        ),

        migrations.RunPython(nullify_datetimefields),

        migrations.AlterField(
            model_name='item',
            name='created_date',
            field=models.DateField(default=date.today),
        ),
        migrations.AlterField(
            model_name='menu',
            name='created_date',
            field=models.DateField(default=date.today),
        ),
        migrations.AlterField(
            model_name='menu',
            name='expiration_date',
            field=models.DateField(blank=True, null=True),
        ),

        migrations.RunPython(set_datefields_from_temp_datefields),

        migrations.RemoveField(
            model_name='item',
            name='temp_created_date',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='temp_created_date',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='temp_expiration_date',
        ),
    ]
