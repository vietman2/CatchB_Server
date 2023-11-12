# Generated by Django 4.2.4 on 2023-11-09 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_uuid', models.UUIDField()),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('anonymous', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forum_name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('allow_anonymous', models.BooleanField(default=False, editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'forum',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_uuid', models.UUIDField()),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('anonymous', models.BooleanField(default=False)),
                ('num_shares', models.IntegerField(default=0)),
                ('num_clicks', models.IntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('forum', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board.forum')),
            ],
            options={
                'db_table': 'post',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_uuid', models.UUIDField()),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('anonymous', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ReCommentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_user_uuid', models.UUIDField()),
                ('report_content', models.TextField()),
                ('recomment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board.recomment')),
            ],
        ),
        migrations.CreateModel(
            name='ReCommentLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_user_uuid', models.UUIDField()),
                ('recomment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board.recomment')),
            ],
        ),
        migrations.CreateModel(
            name='PostReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_user_uuid', models.UUIDField()),
                ('report_content', models.TextField()),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board.post')),
            ],
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_user_uuid', models.UUIDField()),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board.post')),
            ],
        ),
        migrations.CreateModel(
            name='CommentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_user_uuid', models.UUIDField()),
                ('report_content', models.TextField()),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board.comment')),
            ],
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_user_uuid', models.UUIDField()),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board.comment')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board.post'),
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_uuid', models.UUIDField()),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='board.post')),
            ],
        ),
    ]
