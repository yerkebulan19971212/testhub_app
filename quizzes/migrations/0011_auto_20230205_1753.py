# Generated by Django 3.2.12 on 2023-02-05 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizzes', '0010_mark'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoError',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('error_name', models.TextField()),
                ('error_type', models.IntegerField(choices=[(1, 'GRADE'), (2, 'COMPLAIN')])),
            ],
            options={
                'db_table': 'info"."info_error',
            },
        ),
        migrations.CreateModel(
            name='ComplainQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(null=True)),
                ('complain_error', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complain_questions', to='quizzes.infoerror')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complain_questions', to='quizzes.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complain_questions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'info"."complain_question',
            },
        ),
        migrations.AlterField(
            model_name='grade',
            name='grade_error',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grade', to='quizzes.infoerror'),
        ),
        migrations.DeleteModel(
            name='GradeError',
        ),
    ]
