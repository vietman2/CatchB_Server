# Generated by Django 4.2.4 on 2023-12-28 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonsession',
            name='status',
            field=models.CharField(choices=[('PE', '대기'), ('CO', '확정'), ('CA', '취소'), ('FI', '완료')], db_comment='상태', default='PE', max_length=2),
        ),
    ]
