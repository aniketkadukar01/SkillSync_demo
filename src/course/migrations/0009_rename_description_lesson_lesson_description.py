# Generated by Django 5.1.6 on 2025-02-25 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_alter_module_module_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='description',
            new_name='lesson_description',
        ),
    ]
