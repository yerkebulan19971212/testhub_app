# Generated by Django 3.1 on 2022-09-14 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0010_testtypelesson_questions_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionlevel',
            name='choice',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
