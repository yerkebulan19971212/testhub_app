# Generated by Django 3.1 on 2022-09-12 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0009_auto_20220912_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='testtypelesson',
            name='questions_number',
            field=models.IntegerField(default=1),
        ),
    ]