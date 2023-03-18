# Generated by Django 3.2.12 on 2023-03-18 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0027_topic_name_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topicquestion',
            name='question',
        ),
        migrations.RemoveField(
            model_name='topicquestion',
            name='topic',
        ),
        migrations.AddField(
            model_name='lesson',
            name='math',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
        migrations.DeleteModel(
            name='TopicQuestion',
        ),
    ]
