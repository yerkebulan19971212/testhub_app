# Generated by Django 3.2.9 on 2022-10-24 12:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizzes', '0013_alter_testtypelesson_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='PassAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pass_answers', to='quizzes.answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pass_answers', to='quizzes.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pass_answers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'quiz"."pass_answer',
            },
        ),
    ]