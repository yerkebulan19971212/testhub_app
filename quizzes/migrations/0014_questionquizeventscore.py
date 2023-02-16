# Generated by Django 3.2.12 on 2023-02-16 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0013_infoerror_grade_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionQuizEventScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('score', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_event_scores', to='quizzes.question')),
                ('quiz_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_event_score', to='quizzes.quizevent')),
            ],
            options={
                'db_table': 'quiz"."quiz_event_score',
            },
        ),
    ]
