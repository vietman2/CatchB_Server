# Generated by Django 4.2.11 on 2024-03-25 02:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_alter_comment_commenter_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentlike',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_likes', to='comment.comment'),
        ),
    ]
