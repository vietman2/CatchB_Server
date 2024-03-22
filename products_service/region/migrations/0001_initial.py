# Generated by Django 4.2.11 on 2024-03-18 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sido',
            fields=[
                ('sido_code', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('sido_name', models.CharField(max_length=20)),
                ('label', models.CharField(max_length=2)),
                ('display', models.CharField(max_length=4)),
            ],
            options={
                'db_table': 'sido',
            },
        ),
        migrations.CreateModel(
            name='Sigungu',
            fields=[
                ('sigungu_code', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('sigungu_name', models.CharField(max_length=20)),
                ('sido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='region.sido')),
            ],
            options={
                'db_table': 'sigungu',
            },
        ),
    ]
