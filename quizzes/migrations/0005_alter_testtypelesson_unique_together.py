# Generated by Django 3.2.12 on 2022-07-21 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0004_auto_20220722_0047'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='testtypelesson',
            unique_together={('test_type', 'lesson')},
        ),
    ]
