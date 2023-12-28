# Generated by Django 4.2.4 on 2023-12-28 06:18

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import user.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(db_comment='아이디', help_text='Required. 4~20. Letters, digits and @/./+/-/_ only.', max_length=20, unique=True, validators=[user.validators.CustomUsernameValidator(), django.core.validators.MinLengthValidator(4)])),
                ('first_name', models.CharField(db_comment='이름', max_length=50)),
                ('last_name', models.CharField(db_comment='성', max_length=50)),
                ('email', models.EmailField(db_comment='이메일', max_length=254, unique=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(db_comment='전화번호', max_length=128, region=None, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, db_comment='가입일')),
                ('nickname', models.CharField(blank=True, db_comment='닉네임', max_length=150, null=True)),
                ('birth_date', models.DateField(blank=True, db_comment='생년월일', null=True)),
                ('gender', models.CharField(blank=True, db_comment='성별', max_length=1, null=True)),
                ('experience_tier', models.IntegerField(choices=[(0, '미입력'), (1, '초보'), (2, '중급'), (3, '고급')], db_comment='야구 경험 등급', default=0)),
                ('register_route', models.IntegerField(choices=[(0, '미입력'), (1, '캐치비'), (2, '카카오'), (3, '네이버')], db_comment='가입 경로', default=0)),
                ('is_superuser', models.BooleanField(db_comment='슈퍼유저 여부', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('is_active', models.BooleanField(db_comment='계정 활성화 여부', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='coach', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('academic_background', models.TextField(db_comment='학력', help_text='학력을 입력해주세요.')),
                ('baseball_career', models.TextField(db_comment='야구 경력', help_text='야구 경력을 입력해주세요.')),
                ('coaching_career', models.TextField(db_comment='코칭 경력', help_text='코칭 경력을 입력해주세요.')),
                ('is_approved', models.BooleanField(db_comment='코치 승인 여부', default=False)),
            ],
            options={
                'verbose_name': 'coach',
                'verbose_name_plural': 'coaches',
                'db_table': 'coach',
            },
        ),
        migrations.CreateModel(
            name='Counselor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='counselor', serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'counselor',
                'verbose_name_plural': 'counselors',
                'db_table': 'counselor',
            },
            bases=('user.customuser',),
        ),
        migrations.CreateModel(
            name='FacilityOwner',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='facility_owner', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('facility_name', models.CharField(db_comment='시설명', max_length=150)),
                ('facility_address', models.CharField(db_comment='시설 주소', max_length=150)),
                ('facility_phone_number', phonenumber_field.modelfields.PhoneNumberField(db_comment='시설 전화번호', max_length=128, region=None)),
            ],
            options={
                'verbose_name': 'facility_owner',
                'verbose_name_plural': 'facility_owners',
                'db_table': 'facility_owner',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='partner', serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'partner',
                'verbose_name_plural': 'partners',
                'db_table': 'partner',
            },
        ),
    ]
