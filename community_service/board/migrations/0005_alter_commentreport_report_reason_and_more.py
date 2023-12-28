# Generated by Django 4.2.4 on 2023-12-28 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_insert_init_forums'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentreport',
            name='report_reason',
            field=models.CharField(choices=[('AD', '광고'), ('SP', '스팸'), ('AV', '성인물'), ('VI', '폭력적인 내용'), ('IL', '불법적인 내용'), ('OT', '기타')], default='OT', max_length=2),
        ),
        migrations.AlterField(
            model_name='forum',
            name='category',
            field=models.CharField(choices=[('RECR', '모집'), ('INFO', '정보'), ('FREE', '자유')], default='FREE', editable=False, max_length=10),
        ),
        migrations.AlterField(
            model_name='postreport',
            name='report_reason',
            field=models.CharField(choices=[('AD', '광고'), ('SP', '스팸'), ('AV', '성인물'), ('VI', '폭력적인 내용'), ('IL', '불법적인 내용'), ('OT', '기타')], default='OT', max_length=2),
        ),
        migrations.AlterField(
            model_name='recommentreport',
            name='report_reason',
            field=models.CharField(choices=[('AD', '광고'), ('SP', '스팸'), ('AV', '성인물'), ('VI', '폭력적인 내용'), ('IL', '불법적인 내용'), ('OT', '기타')], default='OT', max_length=2),
        ),
    ]
