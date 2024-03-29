# Generated by Django 3.2.12 on 2023-03-04 08:45

import base.constant
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0019_favorite_favorite_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='favorite_type',
            field=models.CharField(choices=[('TEST', 'TEST'), ('SEARCH', 'SEARCH'), ('FLASH_CARD', 'FLASH_CARD')], db_index=True, default=base.constant.FavoriteType['TEST'], max_length=15),
        ),
    ]
