# Generated by Django 4.2.10 on 2024-02-20 09:23

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilityinfo',
            name='custom_equipment',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), db_comment='커스텀 장비', default=list, size=None),
        ),
    ]
