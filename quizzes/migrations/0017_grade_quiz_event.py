# Generated by Django 3.2.12 on 2023-02-19 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0016_grade_user_variant'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='quiz_event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grade', to='quizzes.quizevent'),
        ),
    ]
