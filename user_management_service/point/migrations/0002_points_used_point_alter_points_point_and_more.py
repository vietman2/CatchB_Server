# Generated by Django 4.2.4 on 2023-11-06 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='points',
            name='used_point',
            field=models.IntegerField(db_comment='사용 포인트', default=0),
        ),
        migrations.AlterField(
            model_name='points',
            name='point',
            field=models.IntegerField(db_comment='적립 포인트', default=0),
        ),
        migrations.AlterField(
            model_name='points',
            name='status',
            field=models.CharField(choices=[('ACTIVE', '사용 가능'), ('PARTIAL', '부분 사용'), ('USED', '사용 완료'), ('EXPIRED', '기한 만료')], default='ACTIVE', max_length=10),
        ),
    ]
