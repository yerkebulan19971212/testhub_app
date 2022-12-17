# Generated by Django 3.2.12 on 2022-12-17 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonquestionlevel',
            name='question_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_question_level', to='quizzes.questionlevel'),
        ),
        migrations.AlterField(
            model_name='lessonquestionlevel',
            name='test_type_lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_question_level', to='quizzes.testtypelesson'),
        ),
        migrations.AlterField(
            model_name='question',
            name='lesson_question_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quizzes.lessonquestionlevel'),
        ),
        migrations.AlterField(
            model_name='variantquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant_questions', to='quizzes.question'),
        ),
        migrations.AlterField(
            model_name='variantquestion',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant_questions', to='quizzes.variant'),
        ),
        migrations.CreateModel(
            name='QuestionScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('score', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_score', to='quizzes.question')),
                ('user_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_score', to='quizzes.uservariant')),
            ],
            options={
                'db_table': 'quiz"."score',
            },
        ),
    ]
