# Generated by Django 4.0.3 on 2023-10-30 18:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mtcereports', '0005_job_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_description',
            field=models.TextField(help_text='Describe the work done in detail', max_length=500),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='position',
            field=models.CharField(choices=[('DIR', 'Director'), ('GM', 'General Manager'), ('MGR', 'Manager'), ('SUP', 'Supervisor'), ('ENG', 'Engineer')], help_text='Select your position', max_length=3),
        ),
        migrations.CreateModel(
            name='MonthContainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_name', models.PositiveIntegerField(help_text='Select year', validators=[django.core.validators.MinValueValidator(2015), django.core.validators.MaxValueValidator(2100)])),
                ('month_name', models.IntegerField(choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], help_text='Select month')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
