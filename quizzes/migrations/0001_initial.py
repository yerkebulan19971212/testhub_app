# Generated by Django 3.2.12 on 2022-10-08 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
            ],
            options={
                'db_table': 'quiz"."common_question',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(db_index=True, default=0)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('name_kz', models.CharField(max_length=255)),
                ('name_ru', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255)),
                ('icon', models.ImageField(upload_to='lesson')),
            ],
            options={
                'db_table': 'quiz"."lesson',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='LessonGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('main', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'quiz"."lesson_group',
            },
        ),
        migrations.CreateModel(
            name='LessonQuestionLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(db_index=True, default=0)),
                ('number_of_questions', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'quiz"."lesson_question_level',
            },
        ),
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
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(db_index=True, default=0)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('question', models.TextField()),
                ('common_question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quizzes.commonquestion')),
                ('lesson_question_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.lessonquestionlevel')),
            ],
            options={
                'db_table': 'quiz"."question',
            },
        ),
        migrations.CreateModel(
            name='QuestionLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('name_kz', models.CharField(max_length=255)),
                ('name_ru', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255)),
                ('point', models.PositiveSmallIntegerField(default=0)),
                ('choice', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'db_table': 'quiz"."question_level',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(db_index=True, default=0)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('name_kz', models.CharField(max_length=255)),
                ('name_ru', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'quiz"."tag',
            },
        ),
        migrations.CreateModel(
            name='TestType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(db_index=True, default=0)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('name_kz', models.CharField(max_length=255)),
                ('name_ru', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255)),
                ('icon', models.ImageField(upload_to='test_type')),
            ],
            options={
                'db_table': 'quiz"."test_type',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(db_index=True, default=0)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('variant', models.IntegerField()),
                ('main', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'quiz"."variant',
            },
        ),
        migrations.CreateModel(
            name='VariantQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(db_index=True, default=0)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.question')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.variant')),
            ],
            options={
                'db_table': 'quiz"."variant_question',
            },
        ),
        migrations.CreateModel(
            name='UserVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.variant')),
            ],
            options={
                'db_table': 'quiz"."user_variant',
            },
        ),
        migrations.CreateModel(
            name='TestTypeLessonGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('lesson_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_type_lesson_groups', to='quizzes.lessongroup')),
                ('test_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_type_lesson_groups', to='quizzes.testtype')),
            ],
            options={
                'db_table': 'quiz"."test_type_lesson_group',
            },
        ),
        migrations.CreateModel(
            name='TestTypeLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('main', models.BooleanField(default=False)),
                ('questions_number', models.IntegerField(default=1)),
                ('lesson', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_type_lessons', to='quizzes.lesson')),
                ('test_type', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_type_lessons', to='quizzes.testtype')),
            ],
            options={
                'unique_together': {('test_type', 'lesson')},
            },
        ),
        migrations.CreateModel(
            name='TagQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(db_index=True, default=0)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('name_kz', models.CharField(max_length=255)),
                ('name_ru', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.question')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.tag')),
            ],
            options={
                'db_table': 'quiz"."tag_question',
            },
        ),
        migrations.AddField(
            model_name='tag',
            name='test_type_lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.testtypelesson'),
        ),
        migrations.AddField(
            model_name='lessonquestionlevel',
            name='question_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.questionlevel'),
        ),
        migrations.AddField(
            model_name='lessonquestionlevel',
            name='test_type_lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.testtypelesson'),
        ),
        migrations.CreateModel(
            name='LessonPair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_pairs', to='quizzes.lesson')),
                ('lesson_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_pairs', to='quizzes.lessongroup')),
            ],
            options={
                'db_table': 'quiz"."lesson_pair',
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
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('answer', models.TextField()),
                ('correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quizzes.question')),
            ],
            options={
                'db_table': 'quiz"."answer',
            },
        ),
    ]
