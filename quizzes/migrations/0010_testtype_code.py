# Generated by Django 3.2.9 on 2022-10-24 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0009_variant_variant_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='testtype',
            name='code',
            field=models.CharField(db_index=True, max_length=125, null=True),
        ),
    ]