# Generated by Django 5.1.6 on 2025-02-26 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_questionoptions_is_correct_delete_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignee',
            name='designation',
        ),
        migrations.RemoveField(
            model_name='course',
            name='course_duration',
        ),
        migrations.RemoveField(
            model_name='course',
            name='no_of_assignee',
        ),
    ]
