# Generated by Django 3.1 on 2022-09-12 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0008_auto_20220827_1959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessonquestionlevel',
            name='lesson',
        ),
        migrations.AddField(
            model_name='lessonquestionlevel',
            name='test_type_lesson',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='quizzes.testtypelesson'),
            preserve_default=False,
        ),
    ]
