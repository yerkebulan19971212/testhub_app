# Generated by Django 3.2.12 on 2023-04-09 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0002_detail_universitydetail'),
        ('quizzes', '0039_variant_generation'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='details',
            field=models.ManyToManyField(through='universities.UniversityDetail', to='universities.Detail'),
        ),
    ]
