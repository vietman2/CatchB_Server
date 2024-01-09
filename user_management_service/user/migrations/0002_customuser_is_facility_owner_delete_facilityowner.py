# Generated by Django 4.2.8 on 2024-01-04 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_facility_owner',
            field=models.BooleanField(db_comment='시설 소유자 여부', default=False),
        ),
        migrations.DeleteModel(
            name='FacilityOwner',
        ),
    ]