# Generated by Django 3.2.12 on 2022-11-26 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0026_variantgroup_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessongroup',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
