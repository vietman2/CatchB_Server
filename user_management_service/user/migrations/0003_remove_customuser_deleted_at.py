# Generated by Django 4.2.9 on 2024-03-06 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='deleted_at',
        ),
    ]
