# Generated by Django 4.2.4 on 2023-11-19 11:41

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('road_address', models.CharField(db_comment='도로명 주소', max_length=255)),
                ('road_address_part1', models.CharField(db_comment='도로명 주소 (행정구역)', max_length=255)),
                ('road_address_part2', models.CharField(db_comment='도로명 주소 (상세영역)', max_length=255)),
                ('eng_address', models.CharField(db_comment='영문 주소', max_length=255)),
                ('jibun_address', models.CharField(db_comment='지번 주소', max_length=255)),
                ('zip_code', models.CharField(db_comment='우편번호', max_length=10)),
                ('sido', models.CharField(db_comment='시/도', max_length=20)),
                ('sigungu', models.CharField(db_comment='시/군/구', max_length=20)),
                ('longitude', models.FloatField(db_comment='Longitude. 경도')),
                ('latitude', models.FloatField(db_comment='Latitude. 위도')),
            ],
            options={
                'verbose_name': '주소',
                'verbose_name_plural': '주소',
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('uuid', models.UUIDField(db_comment='시설 고유번호', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(db_comment='시설 이름', max_length=100)),
                ('owner_uuid', models.UUIDField(db_comment='시설 소유자 유저번호')),
                ('phone', models.CharField(db_comment='시설 전화번호', max_length=20)),
                ('image_urls', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), db_comment='시설 이미지 URL', size=None)),
                ('hashtags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), db_comment='시설 해시태그', size=None)),
                ('coaches', django.contrib.postgres.fields.ArrayField(base_field=models.UUIDField(), db_comment='시설 코치 고유번호 배열', size=None)),
                ('intro', models.TextField(db_comment='시설 소개글')),
                ('description', models.TextField(db_comment='시설 설명')),
                ('is_confirmed', models.BooleanField(db_comment='시설 승인 여부', default=False)),
                ('address', models.ForeignKey(db_comment='시설 주소', on_delete=django.db.models.deletion.DO_NOTHING, to='facility.address')),
            ],
            options={
                'verbose_name': '시설',
                'verbose_name_plural': '시설',
                'db_table': 'facility',
            },
        ),
        migrations.AddIndex(
            model_name='address',
            index=models.Index(fields=['sido'], name='sido_index'),
        ),
        migrations.AddIndex(
            model_name='address',
            index=models.Index(fields=['sigungu'], name='sigungu_index'),
        ),
    ]
