# Generated by Django 3.2.12 on 2023-04-16 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0045_auto_20230416_0051'),
        ('universities', '0009_detailspeciality_specialitydetailinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrantUniversityCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('count', models.IntegerField(default=0)),
                ('university_speciality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grant_university_counts', to='quizzes.universityspeciality')),
                ('year', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grant_university_counts', to='universities.year')),
            ],
            options={
                'db_table': 'universities"."grant_university_count',
            },
        ),
    ]