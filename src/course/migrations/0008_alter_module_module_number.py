# Generated by Django 5.1.6 on 2025-02-24 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_alter_course_course_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='module_number',
            field=models.PositiveIntegerField(),
        ),
    ]
