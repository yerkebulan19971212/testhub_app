# Generated by Django 3.2.12 on 2022-10-08 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0003_alter_lessonquestionlevel_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='lesson'),
        ),
        migrations.AlterField(
            model_name='testtype',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='test_type'),
        ),
    ]
