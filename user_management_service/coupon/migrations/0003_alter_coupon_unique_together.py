# Generated by Django 4.2.9 on 2024-01-09 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0002_couponclass_multiple_use_alter_coupon_issued_at_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='coupon',
            unique_together=set(),
        ),
    ]
