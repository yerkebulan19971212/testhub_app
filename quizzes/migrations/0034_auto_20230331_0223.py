# Generated by Django 3.2.12 on 2023-03-30 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_city_name_code'),
        ('quizzes', '0033_questionanswerimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comfort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('name_kz', models.CharField(max_length=255)),
                ('name_ru', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255)),
                ('name_code', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('icon', models.FileField(upload_to='university')),
                ('is_filter', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'quiz"."comfort',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(db_index=True, default=0)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('name_kz', models.CharField(max_length=255)),
                ('name_ru', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255)),
                ('name_code', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('icon', models.FileField(upload_to='country')),
            ],
            options={
                'db_table': 'quiz"."country',
            },
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(db_index=True, default=0)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('name_kz', models.CharField(max_length=255)),
                ('name_ru', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255)),
                ('name_code', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('icon', models.FileField(upload_to='university')),
                ('short_name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'quiz"."speciality',
            },
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(db_index=True, default=0)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('name_kz', models.CharField(max_length=255)),
                ('name_ru', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255)),
                ('name_code', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('icon', models.FileField(upload_to='university')),
                ('short_name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('description', models.TextField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='universities', to='accounts.city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='universities', to='quizzes.country')),
            ],
            options={
                'db_table': 'quiz"."university',
            },
        ),
        migrations.AlterField(
            model_name='answersign',
            name='name_code',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='commonquestion',
            name='name_code',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='name_code',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='questionlevel',
            name='name_code',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='testtype',
            name='name_code',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='name_code',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='variantgroup',
            name='name_code',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='UniversitySpeciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='university_specialities', to='quizzes.speciality')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='university_specialities', to='quizzes.university')),
            ],
            options={
                'db_table': 'quiz"."university_speciality',
            },
        ),
        migrations.CreateModel(
            name='ComfortUniversity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('comfort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comfort_university', to='quizzes.comfort')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comfort_university', to='quizzes.university')),
            ],
            options={
                'db_table': 'quiz"."comfort_university',
            },
        ),
    ]
