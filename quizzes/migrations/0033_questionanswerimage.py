# Generated by Django 3.2.12 on 2023-03-27 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0032_alter_variantquestion_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionAnswerImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('upload', models.ImageField(upload_to='image/')),
            ],
            options={
                'db_table': 'quiz"."question_answer_image',
            },
        ),
    ]
