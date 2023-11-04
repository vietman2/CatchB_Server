# Generated by Django 4.2.4 on 2023-11-04 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('ACTIVE', '사용 가능'), ('USED', '사용 완료'), ('EXPIRED', '쿠폰 만료')], default='ACTIVE', max_length=10)),
                ('valid_until', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_points', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'points',
                'verbose_name_plural': 'points',
                'db_table': 'points',
            },
        ),
    ]
