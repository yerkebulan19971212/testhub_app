# Generated by Django 3.2.12 on 2022-09-25 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NumberOfQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('numbers', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Нумерация вопросов',
                'verbose_name_plural': 'Нумерация вопросов',
                'db_table': 'quiz"."number_of_questions',
            },
        ),
        migrations.CreateModel(
            name='FlashCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('passed', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flash_cards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Флэш карта',
                'verbose_name_plural': 'Флэш карты',
                'db_table': 'quiz"."flash_card',
            },
        ),
    ]
