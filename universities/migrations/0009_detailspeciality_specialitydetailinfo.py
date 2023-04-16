# Generated by Django 3.2.12 on 2023-04-16 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0045_auto_20230416_0051'),
        ('universities', '0008_grantcount_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailSpeciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('name_kz', models.CharField(max_length=255)),
                ('name_ru', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255)),
                ('name_code', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('icon', models.FileField(upload_to='university_detail')),
                ('is_filter', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'universities"."detail_speciality',
            },
        ),
        migrations.CreateModel(
            name='SpecialityDetailInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(db_index=True, default=0)),
                ('value_kz', models.CharField(max_length=128)),
                ('value_ru', models.CharField(default='', max_length=128)),
                ('value_en', models.CharField(blank=True, default='', max_length=128, null=True)),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speciality_detail_infos', to='universities.detailspeciality')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speciality_detail_infos', to='quizzes.speciality')),
            ],
            options={
                'db_table': 'universities"."speciality_detail_infos',
            },
        ),
    ]
