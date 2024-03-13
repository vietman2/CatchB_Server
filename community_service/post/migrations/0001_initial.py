# Generated by Django 4.2.11 on 2024-03-13 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('image', models.FileField(null=True, upload_to='')),
            ],
            options={
                'db_table': 'image',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('forum', models.IntegerField(choices=[(1, '덕아웃'), (2, '드래프트'), (3, '장터'), (4, '스틸')])),
                ('author_uuid', models.UUIDField()),
                ('title', models.CharField(max_length=40)),
                ('content', models.TextField()),
                ('num_clicks', models.IntegerField(default=0)),
                ('images', models.ManyToManyField(blank=True, to='post.image')),
            ],
            options={
                'db_table': 'post',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forum', models.IntegerField(choices=[(1, '덕아웃'), (2, '드래프트'), (3, '장터'), (4, '스틸')])),
                ('name', models.CharField(max_length=20)),
                ('icon', models.URLField()),
                ('color', models.CharField(max_length=7)),
                ('bgcolor', models.CharField(max_length=7)),
            ],
            options={
                'db_table': 'tag',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Steal',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='post.post')),
                ('video', models.FileField(upload_to='steal_videos')),
            ],
            options={
                'db_table': 'steal',
            },
            bases=('post.post',),
        ),
        migrations.CreateModel(
            name='PostReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('report_user_uuid', models.UUIDField(editable=False)),
                ('report_content', models.TextField()),
                ('report_reason', models.CharField(choices=[('AD', '광고'), ('SP', '스팸'), ('AV', '성인물'), ('VI', '폭력적인 내용'), ('IL', '불법적인 내용'), ('OT', '기타')], default='OT', max_length=2)),
                ('reviewed', models.BooleanField(default=False)),
                ('feedback', models.TextField(null=True)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='post.post')),
            ],
            options={
                'db_table': 'post_report',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='post.tag'),
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_uuid', models.UUIDField(editable=False)),
                ('liked_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
            options={
                'db_table': 'post_like',
                'unique_together': {('post', 'user_uuid')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together={('forum', 'author_uuid', 'title')},
        ),
    ]
