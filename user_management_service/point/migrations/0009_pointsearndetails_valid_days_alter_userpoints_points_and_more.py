# Generated by Django 4.2.9 on 2024-01-11 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point', '0008_create_new_points_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointsearndetails',
            name='valid_days',
            field=models.IntegerField(db_comment='유효기간 (일수))', default=0),
        ),
        migrations.AlterField(
            model_name='userpoints',
            name='points',
            field=models.IntegerField(db_comment='적립 포인트'),
        ),
        migrations.AlterField(
            model_name='userpoints',
            name='valid_until',
            field=models.DateTimeField(),
        ),
    ]
