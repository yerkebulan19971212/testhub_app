# Generated by Django 3.2.12 on 2023-03-31 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0036_remove_speciality_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='universityspeciality',
            name='grant',
            field=models.IntegerField(default=140),
        ),
        migrations.AddField(
            model_name='universityspeciality',
            name='score',
            field=models.IntegerField(default=140),
        ),
    ]
