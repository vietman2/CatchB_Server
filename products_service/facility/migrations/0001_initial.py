# Generated by Django 4.2.11 on 2024-03-22 06:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('region', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('member_uuid', models.UUIDField()),
                ('member_name', models.CharField(max_length=10)),
                ('member_phone', models.CharField(max_length=13)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=13)),
                ('reg_code', models.CharField(editable=False, max_length=12, unique=True)),
                ('road_address_part1', models.CharField(max_length=30)),
                ('road_address_part2', models.CharField(max_length=30)),
                ('building_name', models.CharField(max_length=30)),
                ('eng_address', models.CharField(max_length=80)),
                ('jibun_address', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=5)),
                ('longitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('latitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('map_image', models.ImageField(blank=True, upload_to='')),
                ('is_complete', models.BooleanField(default=False)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='region.sigungu')),
            ],
            options={
                'db_table': 'facility',
            },
        ),
        migrations.CreateModel(
            name='FacilityInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro', models.TextField()),
                ('weekday_open', models.TimeField()),
                ('weekday_close', models.TimeField()),
                ('saturday_open', models.TimeField()),
                ('saturday_close', models.TimeField()),
                ('sunday_open', models.TimeField()),
                ('sunday_close', models.TimeField()),
                ('wifi', models.BooleanField(default=False)),
                ('water', models.BooleanField(default=False)),
                ('free_parking', models.BooleanField(default=False)),
                ('paid_parking', models.BooleanField(default=False)),
                ('resting_area', models.BooleanField(default=False)),
                ('separate_toilet', models.BooleanField(default=False)),
                ('air_conditioner', models.BooleanField(default=False)),
                ('heating', models.BooleanField(default=False)),
                ('locker', models.BooleanField(default=False)),
                ('changing_room', models.BooleanField(default=False)),
                ('shower', models.BooleanField(default=False)),
                ('sauna', models.BooleanField(default=False)),
                ('no_smoking', models.BooleanField(default=False)),
                ('smoking_room', models.BooleanField(default=False)),
                ('kids_room', models.BooleanField(default=False)),
                ('no_kids', models.BooleanField(default=False)),
                ('vending_machine', models.BooleanField(default=False)),
                ('proshop', models.BooleanField(default=False)),
                ('num_mounds', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('num_plates', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('wood_bats', models.BooleanField(default=False)),
                ('aluminium_bats', models.BooleanField(default=False)),
                ('gloves', models.BooleanField(default=False)),
                ('catcher_gear', models.BooleanField(default=False)),
                ('pitching_machine', models.BooleanField(default=False)),
                ('batting_tee', models.BooleanField(default=False)),
                ('helmets', models.BooleanField(default=False)),
                ('speed_gun', models.BooleanField(default=False)),
                ('video_analysis', models.BooleanField(default=False)),
                ('monitor', models.BooleanField(default=False)),
                ('speaker', models.BooleanField(default=False)),
                ('fitness', models.BooleanField(default=False)),
                ('group_lesson', models.BooleanField(default=False)),
                ('private_lesson', models.BooleanField(default=False)),
                ('cleats_allowed', models.BooleanField(default=False)),
                ('outdoor', models.BooleanField(default=False)),
                ('pets_allowed', models.BooleanField(default=False)),
                ('wheelchair', models.BooleanField(default=False)),
                ('facility', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='facility.facility')),
            ],
            options={
                'db_table': 'facility_info',
            },
        ),
        migrations.CreateModel(
            name='FacilityImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.FileField(upload_to='')),
                ('cover', models.BooleanField(default=False)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fac_images', to='facility.facility')),
            ],
            options={
                'db_table': 'facility_image',
            },
        ),
    ]
