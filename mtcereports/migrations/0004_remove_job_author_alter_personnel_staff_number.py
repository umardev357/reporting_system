# Generated by Django 4.0.3 on 2023-10-27 09:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtcereports', '0003_alter_job_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='author',
        ),
        migrations.AlterField(
            model_name='personnel',
            name='staff_number',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999999)]),
        ),
    ]
