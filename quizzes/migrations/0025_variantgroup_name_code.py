# Generated by Django 3.2.12 on 2023-03-11 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0024_question_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='variantgroup',
            name='name_code',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
