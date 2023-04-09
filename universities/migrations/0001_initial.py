# Generated by Django 3.2.12 on 2023-04-09 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quizzes', '0039_variant_generation'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniversityImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image', models.FileField(upload_to='university')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='university_images', to='quizzes.university')),
            ],
            options={
                'db_table': 'universities"."university_image',
            },
        ),
    ]
