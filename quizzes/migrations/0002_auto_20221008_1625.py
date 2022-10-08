# Generated by Django 3.2.12 on 2022-10-08 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonquestion',
            name='file',
            field=models.FileField(blank=True, db_index=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='commonquestion',
            name='text',
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(db_index=True),
        ),
    ]
