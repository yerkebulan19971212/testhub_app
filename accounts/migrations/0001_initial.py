# Generated by Django 3.2.12 on 2022-12-16 15:57

import base.constant
import base.service
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='', validators=[base.service.validate_size_image, base.service.validate_mb_image])),
                ('username', models.CharField(max_length=128, unique=True)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, db_index=True, max_length=11, null=True, unique=True)),
                ('language', models.CharField(choices=[('kz', 'KAZAKH'), ('ru', 'RUSSIAN')], db_index=True, default=base.constant.TestLang['KAZAKH'], max_length=64)),
            ],
            options={
                'db_table': 'accounts"."user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='EmailOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=128)),
                ('otp', models.CharField(editable=False, max_length=40)),
                ('forgot', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('attempts', models.IntegerField(default=0)),
                ('used', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Email OTP Token',
                'verbose_name_plural': 'Email OTP Tokens',
                'db_table': 'accounts"."email_otp',
            },
        ),
        migrations.CreateModel(
            name='PhoneOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('phone', models.CharField(blank=True, max_length=11, unique=True, validators=[django.core.validators.MinLengthValidator(limit_value=11)])),
                ('otp', models.CharField(editable=False, max_length=40)),
                ('forgot', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('attempts', models.IntegerField(default=0)),
                ('used', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Phone OTP Token',
                'verbose_name_plural': 'Phone OTP Tokens',
                'db_table': 'accounts"."phone_otp',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'accounts"."role',
            },
        ),
        migrations.CreateModel(
            name='UserTestType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'accounts"."user_test_type',
            },
        ),
    ]
