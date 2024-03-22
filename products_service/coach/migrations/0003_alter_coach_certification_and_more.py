# Generated by Django 4.2.11 on 2024-03-20 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coach', '0002_coach_is_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coach',
            name='certification',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterUniqueTogether(
            name='coach',
            unique_together={('member_uuid', 'uuid')},
        ),
        migrations.CreateModel(
            name='CoachImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.FileField(upload_to='')),
                ('cover', models.BooleanField(default=False)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coach_images', to='coach.coach')),
            ],
            options={
                'db_table': 'coach_image',
            },
        ),
        migrations.AddField(
            model_name='coachinfo',
            name='images',
            field=models.ManyToManyField(related_name='coach_info', to='coach.coachimage'),
        ),
    ]