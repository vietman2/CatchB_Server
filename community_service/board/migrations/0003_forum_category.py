# Generated by Django 4.2.4 on 2023-11-13 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_alter_comment_options_alter_recomment_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='category',
            field=models.CharField(choices=[('RECRUIT', '모집'), ('INFO', '정보'), ('FREE', '자유')], default='FREE', editable=False, max_length=10),
        ),
    ]
