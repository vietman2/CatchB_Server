# Generated by Django 4.2.9 on 2024-01-10 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0003_alter_coupon_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponclass',
            name='issue_valid_days',
            field=models.IntegerField(default=365),
        ),
        migrations.AlterField(
            model_name='couponclass',
            name='use_valid_days',
            field=models.IntegerField(default=365),
        ),
    ]
