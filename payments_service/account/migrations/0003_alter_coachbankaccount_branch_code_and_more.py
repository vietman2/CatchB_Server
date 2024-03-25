# Generated by Django 4.2.11 on 2024-03-22 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_bank_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachbankaccount',
            name='branch_code',
            field=models.CharField(blank=True, default='', max_length=3),
        ),
        migrations.AlterField(
            model_name='ownerbankaccount',
            name='branch_code',
            field=models.CharField(blank=True, default='', max_length=3),
        ),
        migrations.AlterField(
            model_name='userbankaccount',
            name='branch_code',
            field=models.CharField(blank=True, default='', max_length=3),
        ),
    ]