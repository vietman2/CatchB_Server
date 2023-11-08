# Generated by Django 4.2.4 on 2023-11-07 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CouponType',
            new_name='CouponClass',
        ),
        migrations.AlterModelOptions(
            name='couponclass',
            options={'verbose_name': 'coupon_class', 'verbose_name_plural': 'coupon_classes'},
        ),
        migrations.AddField(
            model_name='coupon',
            name='coupon_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coupon_class', to='coupon.couponclass'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='coupon_type',
            field=models.CharField(choices=[('PERCENTAGE', '할인율'), ('AMOUNT', '할인액')], default='PERCENTAGE', max_length=10),
        ),
        migrations.AlterModelTable(
            name='couponclass',
            table='coupon_class',
        ),
    ]